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
from src.runner import test_provider

console = Console()


def _parse_model_ids(models_str: str | None) -> list[str] | None:
    if not models_str:
        return None
    return [m.strip() for m in models_str.split(",") if m.strip()]


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
    if r.prefill_supported is True:
        console.print(
            f"[green]YES[/green] — \"{r.response_text}\" "
            f"({r.elapsed_seconds:.1f}s)"
        )
    elif r.prefill_supported is False:
        console.print(
            f"[red]NO[/red] — \"{r.response_text}\" "
            f"({r.elapsed_seconds:.1f}s)"
        )
    elif r.error:
        err_short = r.error[:80]
        console.print(f"[yellow]ERR[/yellow] — {err_short}")
    else:
        console.print("[dim]?[/dim]")


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

    # Validate models
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

    display_summary(all_results)

    json_path = export_results_json(all_results)
    console.print(f"\n[dim]JSON results: {json_path}[/dim]")

    md_path = export_markdown_report(all_results)
    console.print(f"[dim]Markdown report: {md_path}[/dim]")


@cli.command()
@click.option("--models", "-m", default=None, help="Comma-separated model IDs. Defaults to all cached.")
def matrix(models: str | None) -> None:
    """Display the support matrix from cached results."""
    from src.runner import load_cached_result
    from src.config import CACHE_DIR, TestResult

    model_ids = _parse_model_ids(models)
    if model_ids is None:
        if not CACHE_DIR.exists():
            console.print("[dim]No cached results found. Run the benchmark first.[/dim]")
            return
        model_ids = []
        for d in sorted(CACHE_DIR.iterdir()):
            if d.is_dir():
                model_ids.append(d.name.replace("--", "/", 1))

    all_results: dict[str, list[TestResult]] = {}
    for mid in model_ids:
        slug = mid.replace("/", "--")
        model_dir = CACHE_DIR / slug
        if not model_dir.exists():
            continue
        results: list[TestResult] = []
        for f in sorted(model_dir.glob("*.json")):
            cached = load_cached_result(mid, f.stem)
            if cached:
                r = TestResult(
                    model_id=cached.get("model_id", mid),
                    provider_name=cached.get("provider_name", f.stem),
                    provider_tag=cached.get("provider_tag", f.stem),
                    prefill_supported=cached.get("prefill_supported"),
                    response_text=cached.get("response_text", ""),
                    error=cached.get("error", ""),
                    elapsed_seconds=cached.get("elapsed_seconds", 0.0),
                    cost_usd=cached.get("cost_usd", 0.0),
                )
                results.append(r)
        if results:
            all_results[mid] = results

    if not all_results:
        console.print("[dim]No results found.[/dim]")
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
    from src.runner import load_cached_result
    from src.config import CACHE_DIR

    model_ids = _parse_model_ids(models)
    if model_ids is None:
        if not CACHE_DIR.exists():
            console.print("[dim]No cached results found.[/dim]")
            return
        model_ids = []
        for d in sorted(CACHE_DIR.iterdir()):
            if d.is_dir():
                model_ids.append(d.name.replace("--", "/", 1))

    all_results: dict[str, list[TestResult]] = {}
    for mid in model_ids:
        slug = mid.replace("/", "--")
        model_dir = CACHE_DIR / slug
        if not model_dir.exists():
            continue
        results: list[TestResult] = []
        for f in sorted(model_dir.glob("*.json")):
            cached = load_cached_result(mid, f.stem)
            if cached:
                r = TestResult(
                    model_id=cached.get("model_id", mid),
                    provider_name=cached.get("provider_name", f.stem),
                    provider_tag=cached.get("provider_tag", f.stem),
                    prefill_supported=cached.get("prefill_supported"),
                    response_text=cached.get("response_text", ""),
                    error=cached.get("error", ""),
                    elapsed_seconds=cached.get("elapsed_seconds", 0.0),
                    cost_usd=cached.get("cost_usd", 0.0),
                )
                results.append(r)
        if results:
            all_results[mid] = results

    if not all_results:
        console.print("[dim]No results found.[/dim]")
        return

    out_path = P(output) if output else None
    path = export_markdown_report(all_results, output_path=out_path)
    console.print(f"[green]Markdown report saved to: {path}[/green]")


if __name__ == "__main__":
    cli()
