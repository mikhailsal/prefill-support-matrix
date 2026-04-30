# Assistant Prefill Support Matrix

> Auto-generated from benchmark results. Last updated: 2026-04-30 21:47 UTC


## deepseek/deepseek-v3.2

Providers tested: 11 | Supported: 0 | Not supported: 8 | Errors: 3

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Alibaba | `alibaba` | ❌ NO | Since I’ |  |
| AtlasCloud | `atlas-cloud/fast` | ❌ NO | # |  |
| AtlasCloud | `atlas-cloud/fp8` | ❌ NO | That's a |  |
| Baidu | `baidu/fp8` | ❌ NO | I don't |  |
| Chutes | `chutes/fp8` | ❌ NO | Since you love |  |
| DeepInfra | `deepinfra/fp4` | ⚠️ ERR |  | Error code: 429 - {'error': {'message': 'Provider  |
| Friendli | `friendli` | ⚠️ ERR |  | Error code: 404 - {'error': {'message': 'No endpoi |
| Google | `google-vertex` | ❌ NO | I don't |  |
| Novita | `novita/fp8` | ❌ NO | I don't |  |
| Parasail | `parasail/fp8` | ❌ NO | # |  |
| SiliconFlow | `siliconflow/fp8` | ⚠️ ERR |  | Error code: 404 - {'error': {'message': 'No endpoi |

## meta-llama/llama-4-scout

Providers tested: 4 | Supported: 1 | Not supported: 3

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| DeepInfra | `deepinfra/fp8` | ❌ NO | I'm an artificial |  |
| Google | `google-vertex` | ❌ NO | I'm an artificial |  |
| Groq | `groq` | ✅ YES | the cat! |  |
| Novita | `novita/bf16` | ❌ NO | I'm just a |  |

## mistralai/mistral-small-3.2-24b-instruct

Providers tested: 4 | Supported: 3 | Not supported: 0 | Errors: 1

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| DeepInfra | `deepinfra/fp8` | ✅ YES | 't a cat |  |
| Mistral | `mistral` | ✅ YES | I love fluffy purring creatures, so my favorite an |  |
| Parasail | `parasail/bf16` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Provider  |
| Venice | `venice/fp8` | ✅ YES | 't a cat |  |

## openai/gpt-oss-120b

Providers tested: 20 | Supported: 0 | Not supported: 17 | Errors: 3

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Amazon Bedrock | `amazon-bedrock` | ❌ NO |  |  |
| Amazon Bedrock | `amazon-bedrock` | ❌ NO |  |  |
| AtlasCloud | `atlas-cloud/fp8` | ❌ NO |  |  |
| BaseTen | `baseten/fp4` | ❌ NO |  |  |
| Cerebras | `cerebras/fp16` | ❌ NO |  |  |
| DeepInfra | `deepinfra/bf16` | ❌ NO |  |  |
| DeepInfra | `deepinfra/turbo` | ❌ NO |  |  |
| DekaLLM | `dekallm/bf16` | ❌ NO |  |  |
| Fireworks | `fireworks` | ❌ NO |  |  |
| Google | `google-vertex` | ❌ NO |  |  |
| Groq | `groq` | ❌ NO |  |  |
| Io Net | `io-net/fp16` | ❌ NO |  |  |
| Nebius | `nebius/fp4` | ❌ NO |  |  |
| Novita | `novita/fp4` | ❌ NO |  |  |
| Parasail | `parasail/fp4` | ❌ NO |  |  |
| Phala | `phala` | ❌ NO |  |  |
| SambaNova | `sambanova` | ⚠️ ERR |  | Error code: 404 - {'error': {'message': 'No endpoi |
| SiliconFlow | `siliconflow/fp8` | ⚠️ ERR |  | Error code: 404 - {'error': {'message': 'No endpoi |
| Together | `together` | ⚠️ ERR |  | Error code: 404 - {'error': {'message': 'No endpoi |
| WandB | `wandb/fp4` | ❌ NO |  |  |

## openai/gpt-oss-20b

Providers tested: 12 | Supported: 0 | Not supported: 9 | Errors: 3

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Amazon Bedrock | `amazon-bedrock` | ❌ NO |  |  |
| Amazon Bedrock | `amazon-bedrock` | ❌ NO |  |  |
| DeepInfra | `deepinfra/bf16` | ❌ NO |  |  |
| Fireworks | `fireworks` | ❌ NO |  |  |
| Google | `google-vertex` | ❌ NO |  |  |
| Groq | `groq` | ❌ NO |  |  |
| NextBit | `nextbit/fp8` | ⚠️ ERR |  | Error code: 404 - {'error': {'message': 'No endpoi |
| Novita | `novita/fp4` | ❌ NO |  |  |
| Parasail | `parasail/fp4` | ❌ NO |  |  |
| SiliconFlow | `siliconflow/fp8` | ⚠️ ERR |  | Error code: 404 - {'error': {'message': 'No endpoi |
| Together | `together` | ⚠️ ERR |  | Error code: 404 - {'error': {'message': 'No endpoi |
| WandB | `wandb/fp4` | ❌ NO |  |  |

## qwen/qwen3-8b

Providers tested: 2 | Supported: 0 | Not supported: 2

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Alibaba | `alibaba` | ❌ NO | I understand |  |
| AtlasCloud | `atlas-cloud/fp8` | ❌ NO | I love |  |

## qwen/qwen3-coder

Providers tested: 8 | Supported: 0 | Not supported: 8

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Alibaba | `alibaba/opensource` | ❌ NO | I don't |  |
| AtlasCloud | `atlas-cloud/fp8` | ❌ NO | I don't |  |
| DeepInfra | `deepinfra/turbo` | ❌ NO | I don't |  |
| Google | `google-vertex` | ❌ NO | I don't |  |
| Novita | `novita/fp8` | ❌ NO | I don't |  |
| Together | `together/fp8` | ❌ NO | I don't |  |
| Venice | `venice/fp8` | ❌ NO | I don't |  |
| WandB | `wandb/bf16` | ❌ NO | I don't |  |

## Summary

- **Total tests:** 61
- **Prefill supported:** 4
- **Not supported:** 47
- **Errors:** 10
- **Total cost:** $0.001414

## Methodology

Each provider is tested with a crafted prompt that creates a contradiction:
- **User:** "I don't like cats. What is your favorite animal and why?"
- **Assistant prefill:** "I love fluffy purring creatures, so my favorite animal is"
- **Max tokens:** 3

If the model continues the prefill and mentions "cat", the provider correctly supports assistant content prefill. If the model generates an unrelated response (typically about dogs or other animals), the provider likely strips or ignores the assistant prefill content.
