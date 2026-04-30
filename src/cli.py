"""CLI for the Prefill Support Matrix benchmark.

Tests assistant content prefill support across OpenRouter providers
and models. Supports parallel execution for fast sweeps.
"""

from __future__ import annotations

import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

import click
from rich.console import Console

from src.config import (
    CACHE_DIR,
    DEFAULT_PARALLEL,
    TestResult,
    ensure_dirs,
    load_api_key,
    load_model_list,
)
from src.matrix import (
    display_full_matrix,
    display_model_results,
    display_summary,
    export_markdown_report,
    export_results_json,
)
from src.openrouter_client import OpenRouterClient
from src.runner import load_cached_result, test_provider

console = Console()


def _parse_model_ids(models_str: str | None) -> list[str] | None:
    if not models_str:
        return None
    return [m.strip() for m in models_str.split(",") if m.strip()]


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
    model_id: str,
    *,
    parallel: int,
    force: bool,
) -> list[TestResult]:
    """Discover providers for a model and test each one."""
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
            r = test_provider(client, model_id, p, force=force)
            _print_result_inline(r)
            results.append(r)
    else:
        n_workers = min(parallel, len(providers))
        with ThreadPoolExecutor(max_workers=n_workers) as pool:
            futures = {
                pool.submit(test_provider, client, model_id, p, force=force): p
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
    model_ids = _parse_model_ids(models)
    if model_ids is None:
        model_ids = load_model_list()

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
    valid_ids: list[str] = []
    for mid in model_ids:
        if client.validate_model(mid):
            console.print(f"  [green]OK[/green] {mid}")
            valid_ids.append(mid)
        else:
            console.print(f"  [red]NOT FOUND[/red] {mid}")

    if not valid_ids:
        console.print("[red]No valid models found. Aborting.[/red]")
        sys.exit(1)

    all_results: dict[str, list[TestResult]] = {}
    for mid in valid_ids:
        results = _run_model(client, mid, parallel=parallel, force=force)
        if results:
            all_results[mid] = results
            display_model_results(mid, results)

    if not all_results:
        console.print("[yellow]No results collected.[/yellow]")
        return

    # Show warnings summary for reasoning leaks and provider mismatches
    _print_warnings_summary(all_results)

    display_summary(all_results)

    json_path = export_results_json(all_results)
    console.print(f"\n[dim]JSON results: {json_path}[/dim]")

    md_path = export_markdown_report(all_results)
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
            "║  reasoning.effort being set to \"none\".                 ║\n"
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


if __name__ == "__main__":
    cli()
