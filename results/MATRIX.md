# Assistant Prefill Support Matrix

> Auto-generated from benchmark results. Last updated: 2026-04-30 22:03 UTC


## qwen/qwen3-8b

Providers tested: 2 | Supported: 0 | Not supported: 2

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Alibaba | `alibaba` | ❌ NO | I love fluffy |  |
| AtlasCloud | `atlas-cloud/fp8` | ❌ NO | I love fluffy |  |

## Summary

- **Total tests:** 2
- **Prefill supported:** 0
- **Not supported:** 2
- **Total cost:** $0.000009

## Methodology

Each provider is tested with a crafted prompt that creates a contradiction:
- **User:** "I don't like cats. What is your favorite animal and why?"
- **Assistant prefill:** "I love fluffy purring creatures, so my favorite animal is"
- **Max tokens:** 3

If the model continues the prefill and mentions "cat", the provider correctly supports assistant content prefill. If the model generates an unrelated response (typically about dogs or other animals), the provider likely strips or ignores the assistant prefill content.
