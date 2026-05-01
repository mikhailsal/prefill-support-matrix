"""CLI for the Prefill Support Matrix benchmark.

Tests assistant content prefill support across OpenRouter providers
and models. Supports parallel execution for fast sweeps.
"""

from __future__ import annotations

import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from typing import Any

import click
from rich.console import Console

from prefill_bench.config import (
    CACHE_DIR,
    DEFAULT_PARALLEL,
    ModelTarget,
    TestResult,
    add_model_to_yaml,
    ensure_dirs,
    load_api_key,
    load_model_targets,
)
from prefill_bench.matrix import (
    display_full_matrix,
    display_model_results,
    display_summary,
    export_markdown_report,
    export_results_json,
)
from prefill_bench.openrouter_client import OpenRouterClient
from prefill_bench.runner import load_cached_result, test_provider

console = Console()


def _parse_model_ids(models_str: str | None) -> list[str] | None:
    if not models_str:
        return None
    return [m.strip() for m in models_str.split(",") if m.strip()]


def _cached_model_ids() -> set[str]:
    """Return the set of model IDs that already have cached results."""
    if not CACHE_DIR.exists():
        return set()
    ids: set[str] = set()
    for d in CACHE_DIR.iterdir():
        if d.is_dir() and any(d.glob("*.json")):
            ids.add(d.name.replace("--", "/", 1))
    return ids


def _load_all_cached() -> dict[str, list[TestResult]]:
    """Load all results from cache directory."""
    if not CACHE_DIR.exists():
        return {}

    all_results: dict[str, list[TestResult]] = {}
    for d in sorted(CACHE_DIR.iterdir()):
        if not d.is_dir():
            continue
        model_id = d.name.replace("--", "/", 1)
        results: list[TestResult] = []
        for f in sorted(d.glob("*.json")):
            cached = load_cached_result(model_id, f.stem)
            if cached:
                r = TestResult(
                    model_id=cached.get("model_id", model_id),
                    provider_name=cached.get("provider_name", f.stem),
                    provider_tag=cached.get("provider_tag", f.stem),
                    prefill_supported=cached.get("prefill_supported"),
                    response_text=cached.get("response_text", ""),
                    error=cached.get("error", ""),
                    elapsed_seconds=cached.get("elapsed_seconds", 0.0),
                    prompt_tokens=cached.get("prompt_tokens", 0),
                    completion_tokens=cached.get("completion_tokens", 0),
                    reasoning_tokens=cached.get("reasoning_tokens", 0),
                    reasoning_content=cached.get("reasoning_content"),
                    cost_usd=cached.get("cost_usd", 0.0),
                    http_status=cached.get("http_status"),
                    resolved_provider=cached.get("resolved_provider"),
                    provider_mismatch=cached.get("provider_mismatch"),
                )
                results.append(r)
        if results:
            all_results[model_id] = results

    return all_results


def _run_model(
    client: OpenRouterClient,
    target: ModelTarget,
    *,
    parallel: int,
    force: bool,
) -> list[TestResult]:
    """Discover providers for a model and test each one."""
    model_id = target.model_id
    console.print(f"\n[bold blue]Discovering providers for {model_id}...[/bold blue]")
    providers = client.fetch_providers(model_id)

    if not providers:
        console.print(f"  [yellow]No providers found for {model_id}[/yellow]")
        return []

    console.print(f"  Found [bold]{len(providers)}[/bold] providers")
    for p in providers:
        console.print(f"    [dim]{p.provider_name} ({p.tag}) — {p.quantization}[/dim]")

    results: list[TestResult] = []

    if parallel <= 1:
        for p in providers:
            console.print(f"  Testing [bold]{p.provider_name}[/bold]...", end=" ")
            r = test_provider(
                client,
                model_id,
                p,
                force=force,
                reasoning=target.reasoning,
                include_reasoning=target.include_reasoning,
                allow_reasoning=target.allow_reasoning,
            )
            _print_result_inline(r)
            results.append(r)
    else:
        n_workers = min(parallel, len(providers))
        with ThreadPoolExecutor(max_workers=n_workers) as pool:
            futures = {
                pool.submit(
                    test_provider,
                    client,
                    model_id,
                    p,
                    force=force,
                    reasoning=target.reasoning,
                    include_reasoning=target.include_reasoning,
                    allow_reasoning=target.allow_reasoning,
                ): p
                for p in providers
            }
            for future in as_completed(futures):
                p = futures[future]
                try:
                    r = future.result()
                except Exception as e:
                    r = TestResult(
                        model_id=model_id,
                        provider_name=p.provider_name,
                        provider_tag=p.tag,
                        error=str(e),
                    )
                console.print(f"  [bold]{p.provider_name}[/bold] ", end="")
                _print_result_inline(r)
                results.append(r)

    return results


def _print_result_inline(r: TestResult) -> None:
    extras: list[str] = []

    if r.provider_mismatch:
        console.print(
            f"[bold red]PROVIDER MISMATCH[/bold red] — {r.provider_mismatch}"
        )
        return

    if r.reasoning_tokens > 0 or r.reasoning_content:
        detail = f"{r.reasoning_tokens} reasoning tokens"
        if r.reasoning_content:
            preview = r.reasoning_content[:40].replace("\n", " ")
            detail += f", content: \"{preview}\""
        extras.append(f"[bold yellow]REASONING LEAK: {detail}[/bold yellow]")

    suffix = f" ({r.elapsed_seconds:.1f}s, ${r.cost_usd:.6f})"

    if r.prefill_supported is True:
        console.print(
            f"[green]YES[/green] — \"{r.response_text}\"{suffix}"
        )
    elif r.prefill_supported is False:
        console.print(
            f"[red]NO[/red] — \"{r.response_text}\"{suffix}"
        )
    elif r.error:
        err_short = r.error[:80]
        console.print(f"[yellow]ERR[/yellow] — {err_short}")
    else:
        console.print("[dim]?[/dim]")

    for extra in extras:
        console.print(f"    {extra}")


@click.group()
def cli() -> None:
    """Prefill Support Matrix: test assistant prefill across OpenRouter providers."""
    pass


@cli.command()
@click.option("--models", "-m", default=None, help="Comma-separated model IDs to test.")
@click.option(
    "--parallel", "-P", default=DEFAULT_PARALLEL, type=int, show_default=True,
    help="Number of concurrent provider tests.",
)
@click.option("--force", "-f", is_flag=True, default=False, help="Re-test even if cached.")
def run(models: str | None, parallel: int, force: bool) -> None:
    """Run the prefill support benchmark."""
    parsed_model_ids = _parse_model_ids(models)
    if parsed_model_ids is None:
        model_targets = load_model_targets()
    else:
        model_targets = [ModelTarget(model_id=mid) for mid in parsed_model_ids]
        for mid in parsed_model_ids:
            if add_model_to_yaml(mid):
                console.print(f"[dim]Added {mid} to configs/models.yaml[/dim]")

    model_ids = [t.model_id for t in model_targets]

    if not model_ids:
        console.print(
            "[red]No models specified. Use --models or create configs/models.yaml.[/red]"
        )
        sys.exit(1)

    api_key = load_api_key()
    client = OpenRouterClient(api_key)
    ensure_dirs()

    console.print(f"\n[bold]Prefill Support Matrix[/bold]")
    console.print(f"  Models: {len(model_ids)}")
    for mid in model_ids:
        console.print(f"    {mid}")
    console.print(f"  Parallel workers: {parallel}")
    if force:
        console.print("  [yellow]Force mode: re-testing all providers[/yellow]")
    console.print()

    console.print("[dim]Validating models against OpenRouter catalog...[/dim]")
    valid_targets: list[ModelTarget] = []
    for target in model_targets:
        if client.validate_model(target.model_id):
            console.print(f"  [green]OK[/green] {target.model_id}")
            valid_targets.append(target)
        else:
            console.print(f"  [red]NOT FOUND[/red] {target.model_id}")

    if not valid_targets:
        console.print("[red]No valid models found. Aborting.[/red]")
        sys.exit(1)

    all_results: dict[str, list[TestResult]] = {}
    for target in valid_targets:
        results = _run_model(client, target, parallel=parallel, force=force)
        if results:
            all_results[target.model_id] = results
            display_model_results(target.model_id, results)

    if not all_results:
        console.print("[yellow]No results collected.[/yellow]")
        return

    # Show warnings summary for reasoning leaks and provider mismatches
    _print_warnings_summary(all_results)

    display_summary(all_results)

    # Export reports from full cache so historical models are preserved.
    all_cached_results = _load_all_cached()
    report_results = all_cached_results if all_cached_results else all_results

    json_path = export_results_json(report_results)
    console.print(f"\n[dim]JSON results: {json_path}[/dim]")

    md_path = export_markdown_report(report_results)
    console.print(f"[dim]Markdown report: {md_path}[/dim]")


def _print_warnings_summary(all_results: dict[str, list[TestResult]]) -> None:
    """Print consolidated warnings for reasoning leaks and provider mismatches."""
    reasoning_leaks: list[tuple[str, str, int, str | None]] = []
    mismatches: list[tuple[str, str, str]] = []

    for model_id, results in all_results.items():
        for r in results:
            if r.reasoning_tokens > 0 or r.reasoning_content:
                reasoning_leaks.append((model_id, r.provider_tag, r.reasoning_tokens, r.reasoning_content))
            if r.provider_mismatch:
                mismatches.append((model_id, r.provider_tag, r.provider_mismatch))

    if reasoning_leaks:
        console.print(
            "\n[bold yellow]"
            "╔══════════════════════════════════════════════════════════╗\n"
            "║  REASONING LEAK WARNING                                 ║\n"
            "║  The following providers used reasoning tokens despite   ║\n"
            "║  configured reasoning controls in the request.           ║\n"
            "║  This wastes tokens and inflates costs.                  ║\n"
            "╚══════════════════════════════════════════════════════════╝"
            "[/bold yellow]"
        )
        for model_id, tag, tokens, content_preview in reasoning_leaks:
            detail = f"{tokens} reasoning tokens"
            if content_preview:
                detail += f" (\"{content_preview[:30]}...\")"
            console.print(f"  [yellow]{model_id} @ {tag}: {detail}[/yellow]")

    if mismatches:
        console.print(
            "\n[bold red]"
            "╔══════════════════════════════════════════════════════════╗\n"
            "║  PROVIDER MISMATCH WARNING                              ║\n"
            "║  The gateway ignored provider constraints. These results ║\n"
            "║  are INVALID and excluded from the matrix.               ║\n"
            "╚══════════════════════════════════════════════════════════╝"
            "[/bold red]"
        )
        for model_id, tag, msg in mismatches:
            console.print(f"  [red]{model_id} @ {tag}: {msg}[/red]")


@cli.command()
@click.option("--models", "-m", default=None, help="Comma-separated model IDs. Defaults to all cached.")
def matrix(models: str | None) -> None:
    """Display the support matrix from cached results."""
    if models:
        model_ids = _parse_model_ids(models)
        # Filter cached results by model ids
        all_cached = _load_all_cached()
        all_results = {mid: rs for mid, rs in all_cached.items() if mid in (model_ids or [])}
    else:
        all_results = _load_all_cached()

    if not all_results:
        console.print("[dim]No results found. Run the benchmark first.[/dim]")
        return

    for mid, results in all_results.items():
        display_model_results(mid, results)

    display_full_matrix(all_results)
    display_summary(all_results)


@cli.command("generate-report")
@click.option("--models", "-m", default=None, help="Comma-separated model IDs. Defaults to all cached.")
@click.option(
    "--output", "-o", default=None, type=click.Path(),
    help="Output path for Markdown. Defaults to results/MATRIX.md.",
)
def generate_report(models: str | None, output: str | None) -> None:
    """Generate a Markdown support matrix report."""
    from pathlib import Path as P

    if models:
        model_ids = _parse_model_ids(models)
        all_cached = _load_all_cached()
        all_results = {mid: rs for mid, rs in all_cached.items() if mid in (model_ids or [])}
    else:
        all_results = _load_all_cached()

    if not all_results:
        console.print("[dim]No results found.[/dim]")
        return

    out_path = P(output) if output else None
    path = export_markdown_report(all_results, output_path=out_path)
    console.print(f"[green]Markdown report saved to: {path}[/green]")


def _format_price_per_million(price_str: str) -> str:
    """Convert OpenRouter per-token price string to $/M tokens display."""
    try:
        per_token = float(price_str)
    except (ValueError, TypeError):
        return "?"
    if per_token == 0:
        return "free"
    if per_token < 0:
        return "var"
    per_million = per_token * 1_000_000
    if per_million >= 100:
        return f"${per_million:.0f}"
    if per_million >= 1:
        return f"${per_million:.2f}"
    return f"${per_million:.4f}"


def _format_model_line(model: dict[str, Any], index: int, total: int) -> str:
    """Format a single model entry for the interactive picker menu."""
    model_id = model.get("id", "?")
    created = model.get("created", 0)
    pricing = model.get("pricing", {})
    ctx = model.get("context_length", 0)

    price_in = _format_price_per_million(pricing.get("prompt", "0"))
    price_out = _format_price_per_million(pricing.get("completion", "0"))

    if created:
        age = datetime.fromtimestamp(created, tz=timezone.utc).strftime("%b %d")
    else:
        age = "  ?  "

    ctx_display = f"{ctx // 1000}k" if ctx >= 1000 else str(ctx)

    idx_width = len(str(total))
    idx_str = str(index).rjust(idx_width)

    model_id_display = model_id[:44]

    return (
        f"{idx_str}. {model_id_display:<44s} "
        f"{price_in:>7s}/{price_out:<7s} "
        f"{ctx_display:>5s} "
        f"{age}"
    )


def _pick_model_interactive(
    models: list[dict[str, Any]],
) -> dict[str, Any] | None:
    """Show an interactive terminal menu to pick a model."""
    from simple_term_menu import TerminalMenu

    entries = [
        _format_model_line(m, i + 1, len(models))
        for i, m in enumerate(models)
    ]

    try:
        menu = TerminalMenu(
            entries,
            title=(
                "\n  Prefill Bench — Pick a model to benchmark\n"
                "  ↑↓ navigate | / search | Enter select | q quit\n"
            ),
            search_key="/",
            show_search_hint=True,
            show_search_hint_text='Press "/" to filter by model name',
            status_bar="  in$/M / out$/M   ctx  date",
        )
        chosen = menu.show()
    except OSError:
        console.print(
            "[red]Interactive picker requires a real terminal (TTY).[/red]\n"
            "[dim]Use 'prefill-bench run -m MODEL_ID' to test a specific model instead.[/dim]"
        )
        sys.exit(1)

    if chosen is None:
        return None
    return models[chosen]


@cli.command()
@click.option(
    "--parallel", "-P", default=DEFAULT_PARALLEL, type=int, show_default=True,
    help="Number of concurrent provider tests.",
)
@click.option("--force", "-f", is_flag=True, default=False, help="Re-test even if cached.")
@click.option("--all", "-a", "show_all", is_flag=True, default=False, help="Show all models, including already tested.")
def pick(parallel: int, force: bool, show_all: bool) -> None:
    """Interactively pick a model from OpenRouter and run the benchmark."""
    api_key = load_api_key()
    client = OpenRouterClient(api_key)

    console.print("[dim]Fetching models from OpenRouter...[/dim]")
    text_models = client.fetch_text_models()

    if not text_models:
        console.print("[red]No text models found on OpenRouter.[/red]")
        sys.exit(1)

    if show_all:
        console.print(
            f"[dim]Found {len(text_models)} text-based models, sorted newest first.[/dim]\n"
        )
    else:
        tested = _cached_model_ids()
        before = len(text_models)
        text_models = [m for m in text_models if m.get("id") not in tested]
        skipped = before - len(text_models)
        console.print(
            f"[dim]Found {before} text-based models, "
            f"hiding {skipped} already tested "
            f"({len(text_models)} remaining). "
            f"Use --all to show everything.[/dim]\n"
        )

    if not text_models:
        console.print("[green]All models have been tested![/green]")
        return

    chosen = _pick_model_interactive(text_models)
    if chosen is None:
        console.print("[dim]No model selected. Exiting.[/dim]")
        return

    model_id = chosen["id"]
    console.print(f"\n[bold green]Selected:[/bold green] {model_id}")

    pricing = chosen.get("pricing", {})
    price_in = _format_price_per_million(pricing.get("prompt", "0"))
    price_out = _format_price_per_million(pricing.get("completion", "0"))
    console.print(
        f"  [dim]Price: {price_in}/M input, {price_out}/M output  |  "
        f"Context: {chosen.get('context_length', '?')}[/dim]"
    )

    if add_model_to_yaml(model_id):
        console.print(f"  [dim]Added {model_id} to configs/models.yaml[/dim]")

    ensure_dirs()
    target = ModelTarget(model_id=model_id)

    console.print(f"\n[bold]Running prefill benchmark for {model_id}...[/bold]")
    results = _run_model(client, target, parallel=parallel, force=force)

    if not results:
        console.print("[yellow]No results collected.[/yellow]")
        return

    all_results = {model_id: results}
    _print_warnings_summary(all_results)
    display_model_results(model_id, results)
    display_summary(all_results)

    all_cached = _load_all_cached()
    report_results = all_cached if all_cached else all_results

    json_path = export_results_json(report_results)
    console.print(f"\n[dim]JSON results: {json_path}[/dim]")
    md_path = export_markdown_report(report_results)
    console.print(f"[dim]Markdown report: {md_path}[/dim]")


if __name__ == "__main__":
    cli()
