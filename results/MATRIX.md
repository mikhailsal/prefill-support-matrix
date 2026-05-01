# Assistant Prefill Support Matrix

> Auto-generated from benchmark results. Last updated: 2026-05-01 11:01 UTC


## qwen/qwen3.5-plus-20260420

Providers tested: 1 | Supported: 0 | Not supported: 1

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Alibaba | `alibaba` | ❌ NO | I don't have personal preferences or feelings, so  |  |

## Summary

- **Total tests:** 1
- **Prefill supported:** 0
- **Not supported:** 1
- **Total cost:** $0.000139

## Methodology

Each provider is tested with a crafted prompt that creates a contradiction:
- **User:** "I don't like cats. What is your favorite animal and why?"
- **Assistant prefill:** "I love fluffy purring creatures, so my favorite animal is"
- **Max tokens:** 50 | **Temperature:** 0.0 | **Reasoning:** disabled

If the model continues the prefill and mentions "cat", the provider correctly supports assistant content prefill. If the model generates an unrelated response (typically about dogs or other animals), the provider likely strips or ignores the assistant prefill content.
