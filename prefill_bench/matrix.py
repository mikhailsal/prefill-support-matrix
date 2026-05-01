"""Matrix: aggregate results and generate support matrix displays.

Provides rich console table output, JSON export, and Markdown report
generation for the prefill support matrix.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.table import Table
from rich.text import Text

from prefill_bench.config import RESULTS_DIR, TestResult

console = Console()

def _status_text(result: TestResult) -> Text:
    if result.provider_mismatch:
        return Text("MISMATCH", style="bold magenta")
    if result.prefill_supported is True:
        return Text("YES", style="bold green")
    elif result.prefill_supported is False:
        return Text("NO", style="bold red")
    elif result.error:
        return Text("ERR", style="bold yellow")
    return Text("?", style="dim")


def _status_str(result: TestResult) -> str:
    if result.provider_mismatch:
        return "MISMATCH"
    if result.prefill_supported is True:
        return "YES"
    elif result.prefill_supported is False:
        return "NO"
    elif result.error:
        return "ERR"
    return "?"


def display_model_results(model_id: str, results: list[TestResult]) -> None:
    """Display results for a single model as a table."""
    if not results:
        console.print(f"[dim]No results for {model_id}[/dim]")
        return

    table = Table(
        title=f"Prefill Support: {model_id}",
        title_style="bold",
        show_lines=False,
        box=None,
        expand=False,
        padding=(0, 1),
    )
    table.add_column("#", justify="right", style="dim", width=3)
    table.add_column("Provider", style="bold", min_width=18, no_wrap=True)
    table.add_column("Tag", style="dim", min_width=14, no_wrap=True)
    table.add_column("Prefill", justify="center", width=10)
    table.add_column("Response", max_width=30, overflow="ellipsis")
    table.add_column("Tokens", justify="right", width=6)
    table.add_column("Cost", justify="right", width=10)
    table.add_column("Time", justify="right", width=6)
    table.add_column("Notes", style="dim", max_width=30, overflow="ellipsis")

    for i, r in enumerate(sorted(results, key=lambda x: x.provider_name), 1):
        response_preview = r.response_text[:30] if r.response_text else ""
        elapsed = f"{r.elapsed_seconds:.1f}s" if r.elapsed_seconds else ""
        cost_str = f"${r.cost_usd:.6f}" if r.cost_usd > 0 else "$0"
        tokens_str = str(r.completion_tokens) if r.completion_tokens else ""

        notes_parts: list[str] = []
        if r.reasoning_tokens > 0:
            notes_parts.append(f"reasoning:{r.reasoning_tokens}t")
        if r.provider_mismatch:
            notes_parts.append("MISMATCH")
        if r.error and not r.provider_mismatch:
            notes_parts.append(r.error[:20])
        notes = " | ".join(notes_parts)

        table.add_row(
            str(i),
            r.provider_name,
            r.provider_tag,
            _status_text(r),
            response_preview,
            tokens_str,
            cost_str,
            elapsed,
            notes,
        )

    console.print(table)
    console.print()


def display_full_matrix(all_results: dict[str, list[TestResult]]) -> None:
    """Display the full model x provider support matrix."""
    if not all_results:
        console.print("[dim]No results to display.[/dim]")
        return

    all_providers: dict[str, str] = {}
    for results in all_results.values():
        for r in results:
            if r.provider_tag not in all_providers:
                all_providers[r.provider_tag] = r.provider_name

    provider_tags = sorted(all_providers.keys())
    if not provider_tags:
        console.print("[dim]No providers found.[/dim]")
        return

    table = Table(
        title="Prefill Support Matrix",
        title_style="bold",
        show_lines=True,
        expand=False,
        padding=(0, 1),
    )
    table.add_column("Model", style="bold", no_wrap=True, min_width=30)
    for tag in provider_tags:
        name = all_providers[tag]
        short_name = name[:12]
        table.add_column(short_name, justify="center", width=5, no_wrap=True)

    for model_id in sorted(all_results.keys()):
        results_by_provider = {r.provider_tag: r for r in all_results[model_id]}
        row: list[str | Text] = [model_id]
        for tag in provider_tags:
            if tag in results_by_provider:
                row.append(_status_text(results_by_provider[tag]))
            else:
                row.append(Text("-", style="dim"))
        table.add_row(*row)

    console.print(table)


def display_summary(all_results: dict[str, list[TestResult]]) -> None:
    """Display aggregate statistics."""
    total_tests = 0
    total_yes = 0
    total_no = 0
    total_err = 0
    total_cost = 0.0

    for results in all_results.values():
        for r in results:
            total_tests += 1
            total_cost += r.cost_usd
            if r.prefill_supported is True:
                total_yes += 1
            elif r.prefill_supported is False:
                total_no += 1
            else:
                total_err += 1

    console.print(f"\n[bold]Summary[/bold]")
    console.print(f"  Total tests: {total_tests}")
    console.print(f"  [green]Prefill supported: {total_yes}[/green]")
    console.print(f"  [red]Prefill NOT supported: {total_no}[/red]")
    if total_err:
        console.print(f"  [yellow]Errors: {total_err}[/yellow]")
    console.print(f"  Total cost: ${total_cost:.6f}")


# ---------------------------------------------------------------------------
# Markdown export
# ---------------------------------------------------------------------------

def generate_markdown_report(all_results: dict[str, list[TestResult]]) -> str:
    """Generate a Markdown support matrix report."""
    if not all_results:
        return "No results available yet. Run the benchmark first.\n"

    def _sanitize_md_cell(text: str, max_len: int = 50) -> str:
        """Sanitize markdown table cell content."""
        # Keep table rows stable when providers return multiline content.
        return text.replace("\r\n", "\n").replace("\r", "\n").replace("\n", " [NL] ").replace("|", "\\|")[:max_len]

    lines: list[str] = []
    lines.append("# Assistant Prefill Support Matrix\n")
    lines.append(
        f"> Auto-generated from benchmark results. "
        f"Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n"
    )
    lines.append("")

    # Collect all providers
    all_providers: dict[str, str] = {}
    for results in all_results.values():
        for r in results:
            if r.provider_tag not in all_providers:
                all_providers[r.provider_tag] = r.provider_name

    # Per-model tables
    for model_id in sorted(all_results.keys()):
        results = all_results[model_id]
        lines.append(f"## {model_id}\n")

        yes_count = sum(1 for r in results if r.prefill_supported is True)
        no_count = sum(1 for r in results if r.prefill_supported is False)
        err_count = sum(1 for r in results if r.prefill_supported is None)
        lines.append(
            f"Providers tested: {len(results)} | "
            f"Supported: {yes_count} | "
            f"Not supported: {no_count}"
            + (f" | Errors: {err_count}" if err_count else "")
            + "\n"
        )

        lines.append("| Provider | Tag | Prefill | Response | Error |")
        lines.append("|----------|-----|:-------:|----------|-------|")

        for r in sorted(results, key=lambda x: x.provider_name):
            status = _status_str(r)
            icon = {"YES": "✅", "NO": "❌", "ERR": "⚠️"}.get(status, "❓")
            response = _sanitize_md_cell(r.response_text) if r.response_text else ""
            error = _sanitize_md_cell(r.error) if r.error else ""
            lines.append(
                f"| {r.provider_name} | `{r.provider_tag}` | {icon} {status} | {response} | {error} |"
            )

        lines.append("")

    # Summary stats
    total = sum(len(rs) for rs in all_results.values())
    total_yes = sum(1 for rs in all_results.values() for r in rs if r.prefill_supported is True)
    total_no = sum(1 for rs in all_results.values() for r in rs if r.prefill_supported is False)
    total_err = sum(1 for rs in all_results.values() for r in rs if r.prefill_supported is None)
    total_cost = sum(r.cost_usd for rs in all_results.values() for r in rs)

    lines.append("## Summary\n")
    lines.append(f"- **Total tests:** {total}")
    lines.append(f"- **Prefill supported:** {total_yes}")
    lines.append(f"- **Not supported:** {total_no}")
    if total_err:
        lines.append(f"- **Errors:** {total_err}")
    lines.append(f"- **Total cost:** ${total_cost:.6f}")
    lines.append("")

    lines.append("## Methodology\n")
    lines.append("Each provider is tested with a crafted prompt that creates a contradiction:")
    lines.append("- **User:** \"I don't like cats. What is your favorite animal and why?\"")
    lines.append("- **Assistant prefill:** \"I love fluffy purring creatures, so my favorite animal is\"")
    lines.append("- **Max tokens:** 50 | **Temperature:** 0.0 | **Reasoning:** disabled\n")
    lines.append(
        "If the model continues the prefill sentence (starting lowercase, e.g. "
        "\"the cat\", \"the red panda\", \"a dog!\"), the provider correctly supports "
        "assistant content prefill. If the model generates a fresh response starting "
        "with a capital letter (e.g. \"I don't have preferences\"), the provider likely "
        "strips or ignores the assistant prefill content.\n"
    )

    return "\n".join(lines)


def export_markdown_report(
    all_results: dict[str, list[TestResult]],
    *,
    output_path: Path | None = None,
) -> Path:
    md = generate_markdown_report(all_results)
    if output_path is None:
        output_path = RESULTS_DIR / "MATRIX.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(md, encoding="utf-8")
    return output_path


def export_results_json(all_results: dict[str, list[TestResult]]) -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    path = RESULTS_DIR / f"results_{timestamp}.json"

    data: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "benchmark": "prefill_support_matrix",
        "models": {},
    }

    for model_id in sorted(all_results.keys()):
        providers = []
        for r in sorted(all_results[model_id], key=lambda x: x.provider_name):
            providers.append({
                "provider_name": r.provider_name,
                "provider_tag": r.provider_tag,
                "prefill_supported": r.prefill_supported,
                "response_text": r.response_text,
                "error": r.error,
                "elapsed_seconds": round(r.elapsed_seconds, 3),
                "prompt_tokens": r.prompt_tokens,
                "completion_tokens": r.completion_tokens,
                "reasoning_tokens": r.reasoning_tokens,
                "cost_usd": round(r.cost_usd, 8),
                "resolved_provider": r.resolved_provider,
                "provider_mismatch": r.provider_mismatch,
            })
        data["models"][model_id] = providers

    total_cost = sum(r.cost_usd for rs in all_results.values() for r in rs)
    data["total_cost_usd"] = round(total_cost, 6)

    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path
