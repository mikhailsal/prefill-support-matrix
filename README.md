# Prefill Support Matrix

**Which LLM providers actually support assistant prefill — and which silently strip it?**

We tested **279 API calls** across **50+ models** and **40+ providers** on [OpenRouter](https://openrouter.ai/) to find out. The entire benchmark cost **$0.04**.

| Metric | Value |
|--------|-------|
| Models tested | 50+ |
| Providers tested | 40+ |
| Total API calls | 279 |
| Prefill supported | 94 (34%) |
| Prefill stripped | 95 (34%) |
| Errors | 90 (32%) |
| Total cost | $0.043 |

> **[View the full support matrix →](results/MATRIX.md)**

---

## Key Findings

### 1. Prefill support is provider-dependent, not model-dependent

The same model can support prefill on one provider and silently ignore it on another. **DeepSeek V3.2** is the most dramatic example: 11 providers tested, only **1** (SiliconFlow) passes prefill through — the other 10 strip it without any error or warning.

### 2. Anthropic models have near-perfect prefill support

Claude Haiku 4.5, Opus 4.5, and Sonnet 4.5 all support prefill across every provider that successfully serves them — Anthropic native, Amazon Bedrock, and Google Vertex. If your application relies on constrained generation via prefill, Anthropic is the safest bet.

### 3. OpenAI models reject prefill entirely

Every OpenAI model tested — GPT-5.3-chat, GPT-5.3-codex, GPT-5.4-nano, GPT-OSS-120b, GPT-OSS-20b — shows **zero** prefill support. The open-source GPT-OSS models additionally fail with "Reasoning" errors on most providers (15/19 for the 120B variant).

### 4. Z.AI/GLM models are surprisingly excellent

`z-ai/glm-5` achieves **14/14** prefill support on all providers that responded successfully. `glm-5.1` hits 12/13. These models offer some of the most consistent prefill behavior in the entire benchmark — and they're cheap.

### 5. Reasoning mode and prefill are incompatible on many providers

A huge portion of errors come from providers rejecting prefill when reasoning/thinking mode is enabled. This affects GPT-OSS, Minimax M2.5/M2.7, Grok-3-mini, Google Gemini Pro, and others. If you need prefill, you must disable reasoning.

### 6. Third-party providers strip prefill for Qwen and Gemma models

Google Gemma-4 models show 0% prefill support across 8–10 third-party providers (DeepInfra, Novita, Parasail, Together, Venice, etc.) — yet the free Google AI Studio tier supports it fine. Qwen 3.5/3.6 models follow the same pattern. These inference providers are stripping the assistant message during preprocessing.

---

## How It Works

The benchmark exploits a simple psychological contradiction to create an unmistakable signal:

```
User:              "I don't like cats. What is your favorite animal and why?"
Assistant prefill: "I love fluffy purring creatures, so my favorite animal is"
Max tokens:        50
```

**If prefill works:** The model *must* continue from "...my favorite animal is" — and since the prefill already committed to "fluffy purring creatures," it invariably says **"cat"** (or similar feline). The response starts lowercase, continuing the sentence.

**If prefill is stripped:** The model starts fresh, sees the user dislikes cats, and picks a different animal (dogs, dolphins, octopuses). The response starts with a capital letter as a new sentence.

This design makes false positives nearly impossible — a model would have to independently choose cats despite the user explicitly disliking them *and* happen to start with a lowercase continuation. In 279 tests, this never occurred.

### What counts as a positive result?

The detection logic checks whether the response text begins with a lowercase letter (continuing the prefill sentence) or an uppercase letter / special character (starting fresh). Combined with the semantic contradiction, this simple heuristic achieves effectively 100% accuracy.

### Why is it so cheap?

Each test uses ~34 prompt tokens and exactly 50 completion tokens. At typical API pricing, each call costs a fraction of a cent. The entire 279-call benchmark totals **$0.043** — you could run it hundreds of times for under a dollar.

---

## Run It Yourself

The benchmark is designed to be trivially reproducible. You need one environment variable and one command.

### Setup

```bash
pip install -e .
echo "OPENROUTER_KEY=your-key-here" > .env
```

### Run

```bash
# Test all models from configs/models.yaml against all their providers
prefill-bench run

# Run with 32 parallel workers (default: 16)
prefill-bench run -P 32

# Test specific models only
prefill-bench run --models "deepseek/deepseek-v3.2,anthropic/claude-haiku-4.5"

# Force re-test (ignore cache)
prefill-bench run --force

# Interactive model picker — browse all OpenRouter models
prefill-bench pick
```

### View Results

```bash
# Print matrix to terminal
prefill-bench matrix

# Export Markdown report to results/
prefill-bench generate-report
```

Results are cached per model+provider pair in `cache/`, so re-running only tests new combinations.

---

## Configuration

### Environment Variables

Create a `.env` file:

```
OPENROUTER_KEY=your-openrouter-api-key
```

### Model List

Edit `configs/models.yaml` to choose which models to test:

```yaml
models:
  - deepseek/deepseek-v3.2         # plain string — test all providers
  - id: x-ai/grok-4.1-fast         # object form — with per-model options
    allow_reasoning: true
```

The benchmark auto-discovers all available providers for each model via OpenRouter's endpoints API. You don't need to specify providers manually.

---

## Project Structure

```
├── configs/
│   └── models.yaml              # Models to benchmark
├── prefill_bench/
│   ├── cli.py                   # Click CLI with thread pool
│   ├── config.py                # Configuration and data classes
│   ├── matrix.py                # Results aggregation and display
│   ├── openrouter_client.py     # OpenRouter API client
│   └── runner.py                # Per-provider test logic
├── cache/                       # Cached results (one JSON per test)
├── results/
│   └── MATRIX.md                # Generated support matrix
├── pyproject.toml
└── README.md
```

---

## License

MIT
