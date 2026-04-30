# Prefill Support Matrix

Automated benchmark that tests **assistant content prefill** support across different providers and models on [OpenRouter](https://openrouter.ai/).

Assistant prefill is the ability to include a partial assistant message in the API request that the model continues from, rather than generating a fresh response. This is a critical feature for constrained generation, format enforcement, and prompt engineering techniques — but not all providers support it.

## How It Works

The benchmark sends a crafted prompt designed to create a clear contradiction:

- **User:** `"I don't like cats. What is your favorite animal and why?"`
- **Assistant prefill:** `"I love fluffy purring creatures, so my favorite animal is"`
- **Max tokens:** 3

If the provider correctly handles the assistant prefill, the model must continue from `"...my favorite animal is"` and will say **"cat"** (since the prefill already committed to "fluffy purring creatures").

If the provider strips or ignores the prefill, the model starts fresh and — given the user's stated dislike of cats — will typically pick a different animal (dogs, dolphins, etc.).

This approach is:
- **Cheap** — only 3 completion tokens per test
- **Deterministic** — the contradiction makes false positives nearly impossible
- **Fast** — sub-second per provider with parallelism

## Quick Start

```bash
# Install
pip install -e .

# Run with default model list from configs/models.yaml
prefill-bench run

# Run specific models
prefill-bench run --models "meta-llama/llama-4-scout,mistralai/mistral-small-3.2-24b-instruct"

# Run with 32 parallel workers
prefill-bench run -P 32

# Force re-test (ignore cache)
prefill-bench run --force

# View cached results as a matrix
prefill-bench matrix

# Export Markdown report
prefill-bench generate-report
```

## Configuration

### Environment Variables

Create a `.env` file:

```
OPENROUTER_KEY=your-proxy-key
```

### Model List

Edit `configs/models.yaml`:

```yaml
models:
  - openai/gpt-oss-120b
  - meta-llama/llama-4-scout
  - mistralai/mistral-small-3.2-24b-instruct
```

The benchmark auto-discovers all available providers for each model via the OpenRouter endpoints API.

## Results

Results are cached in `cache/` (one JSON file per model+provider pair) and exported to `results/`:
- `results/MATRIX.md` — Markdown support matrix
- `results/results_*.json` — Full JSON results with timestamps

## Project Structure

```
├── configs/
│   └── models.yaml          # Models to test
├── src/
│   ├── cli.py               # Click CLI with threading
│   ├── config.py            # Configuration and data classes
│   ├── matrix.py            # Results aggregation and display
│   ├── openrouter_client.py # OpenRouter API client
│   └── runner.py            # Per-provider test logic
├── cache/                   # Cached test results (gitignored)
├── results/                 # Exported reports
├── pyproject.toml
└── README.md
```

## License

MIT
