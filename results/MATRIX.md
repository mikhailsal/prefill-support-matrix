# Assistant Prefill Support Matrix

> Auto-generated from benchmark results. Last updated: 2026-05-01 20:32 UTC


## aion-labs/aion-2.0

Providers tested: 1 | Supported: 0 | Not supported: 0 | Errors: 1

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| AionLabs | `aion-labs` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |

## anthropic/claude-3.5-haiku

Providers tested: 2 | Supported: 2 | Not supported: 0

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Amazon Bedrock | `amazon-bedrock` | ✅ YES | the cat! They're adorable, playful, and have such  |  |
| Google | `google-vertex` | ✅ YES | the red panda! They're adorable, with reddish-brow |  |

## anthropic/claude-haiku-4.5

Providers tested: 4 | Supported: 4 | Not supported: 0

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Amazon Bedrock | `amazon-bedrock` | ✅ YES | the cat. But I'm curious what draws you away from  |  |
| Anthropic | `anthropic` | ✅ YES | the cat. But I'm curious what draws you away from  |  |
| Google | `google-vertex/europe` | ✅ YES | the cat. But I'm curious what draws you away from  |  |
| Google | `google-vertex` | ✅ YES | the cat. But I'm curious what draws you away from  |  |

## anthropic/claude-opus-4.5

Providers tested: 4 | Supported: 4 | Not supported: 0

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Amazon Bedrock | `amazon-bedrock` | ✅ YES | the cat. Just kidding! I don't actually have perso |  |
| Anthropic | `anthropic/2` | ✅ YES | the cat. Just kidding! I don't actually have perso |  |
| Anthropic | `anthropic` | ✅ YES | the cat. Just kidding! Since you mentioned you're  |  |
| Google | `google-vertex` | ✅ YES | the cat. Just kidding! Since you mentioned you're  |  |

## anthropic/claude-opus-4.7

Providers tested: 5 | Supported: 0 | Not supported: 0 | Errors: 5

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Amazon Bedrock | `amazon-bedrock` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'This mode |
| Anthropic | `anthropic/2` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'This mode |
| Anthropic | `anthropic` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'This mode |
| Google | `google-vertex/europe` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'This mode |
| Google | `google-vertex` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'This mode |

## anthropic/claude-sonnet-4.5

Providers tested: 5 | Supported: 3 | Not supported: 0 | Errors: 2

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Amazon Bedrock | `amazon-bedrock` | ✅ YES | ... the red panda!  [NL]  [NL] They have that perf |  |
| Anthropic | `anthropic/2` | ✅ YES | ... the red panda! [NL]  [NL] They're these adorab |  |
| Anthropic | `anthropic` | ✅ YES | ... the red panda! [NL]  [NL] They're these adorab |  |
| Google | `google-vertex/global` | ❓ MISMATCH | ... the red panda! [NL]  [NL] They're these adorab | Provider mismatch: requested 'google-vertex/global |
| Google | `google-vertex` | ❓ MISMATCH | ... the red panda! [NL]  [NL] They're these adorab | Provider mismatch: requested 'google-vertex', gate |

## arcee-ai/trinity-large-thinking

Providers tested: 3 | Supported: 0 | Not supported: 0 | Errors: 3

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Arcee AI | `arcee-ai` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Parasail | `parasail/fp8` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Venice | `venice/fp8` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |

## baidu/qianfan-ocr-fast:free

Providers tested: 1 | Supported: 1 | Not supported: 0

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Baidu | `baidu/fp8` | ✅ YES | I love fluffy purring creatures, so my favorite animal is |  |

## bytedance-seed/seed-2.0-lite

Providers tested: 1 | Supported: 1 | Not supported: 0

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Seed | `seed/fp8` | ✅ YES | the cat! I’m really fond of their independent natu |  |

## deepseek/deepseek-v3.1-terminus

Providers tested: 4 | Supported: 3 | Not supported: 0 | Errors: 1

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| AtlasCloud | `atlas-cloud/fp8` | ✅ YES | the **red panda**! Here’s why: [NL]  [NL] 1. **The |  |
| DeepInfra | `deepinfra/fp4` | ⚠️ ERR |  | Request timed out. |
| Novita | `novita/fp8` | ✅ YES | actually a cat! But I completely understand they'r |  |
| SiliconFlow | `siliconflow/fp8` | ✅ YES | the **red panda**! [NL]  [NL] Here’s why I find th |  |

## deepseek/deepseek-v3.2

Providers tested: 11 | Supported: 1 | Not supported: 10

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Alibaba | `alibaba` | ❌ NO | Given your preference for fluffy, purring creature |  |
| AtlasCloud | `atlas-cloud/fast` | ❌ NO | # 1. 两数之和 [NL]  [NL] ## 题目 [NL]  [NL] 给定一个整数数组 num |  |
| AtlasCloud | `atlas-cloud/fp8` | ❌ NO | That's a wonderful choice! While I don't have pers |  |
| Baidu | `baidu/fp8` | ❌ NO | I understand you don't like cats, and that's perfe |  |
| Chutes | `chutes/fp8` | ❌ NO | Since you love fluffy, purring creatures, I’d say  |  |
| DeepInfra | `deepinfra/fp4` | ❌ NO | <｜begin▁of▁sentence｜># 1. 两数之和 [NL]  [NL] ## 题目 [N |  |
| Friendli | `friendli` | ❌ NO | # 1. 两数之和 [NL]  [NL] ## 题目 [NL]  [NL] 给定一个整数数组 `nu |  |
| Google | `google-vertex` | ❌ NO | I don't have personal preferences or feelings, but |  |
| Novita | `novita/fp8` | ❌ NO | That's a wonderful choice! Since you love fluffy,  |  |
| Parasail | `parasail/fp8` | ❌ NO | # 1. 两数之和 [NL]  [NL] ## 题目 [NL]  [NL] 给定一个整数数组 `nu |  |
| SiliconFlow | `siliconflow/fp8` | ✅ YES | the **red panda**! Here’s why: [NL]  [NL] *   **Th |  |

## deepseek/deepseek-v3.2-exp

Providers tested: 3 | Supported: 3 | Not supported: 0

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| AtlasCloud | `atlas-cloud/fp8` | ✅ YES | the **red panda**! Here’s why: [NL]  [NL] 1. **The |  |
| Novita | `novita/fp8` | ✅ YES | the **red panda**! Here’s why: [NL]  [NL] 1. **The |  |
| SiliconFlow | `siliconflow/fp8` | ✅ YES | the **red panda**! Here’s why: [NL]  [NL] *   **Th |  |

## deepseek/deepseek-v4-flash

Providers tested: 7 | Supported: 2 | Not supported: 4 | Errors: 1

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| AkashML | `akashml/fp8` | ⚠️ ERR |  | Error code: 429 - {'error': {'message': 'Provider  |
| AtlasCloud | `atlas-cloud/fp8` | ✅ YES | …orite animal is the **red panda**! They're like a mix of a cat, a rac |  |
| DeepInfra | `deepinfra/fp4` | ❌ NO | # My Favorite Animal: The Octopus [NL]  [NL] While |  |
| DeepSeek | `deepseek` | ✅ YES | the cat! But since you don't share that preference |  |
| Novita | `novita` | ❌ NO | 💭 P. S. I don't actually have personal preferences |  |
| Parasail | `parasail/fp8` | ❌ NO | 8=D |  |
| SiliconFlow | `siliconflow/fp8` | ❌ NO | I don't have personal feelings or preferences, so  |  |

## deepseek/deepseek-v4-pro

Providers tested: 7 | Supported: 0 | Not supported: 1 | Errors: 6

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| AtlasCloud | `atlas-cloud/fp8` | ❓ MISMATCH | 💭 …orite animal is ". It seems cut off. The assistant message | Provider mismatch: requested 'atlas-cloud/fp8', ga |
| DeepSeek | `deepseek` | ❓ MISMATCH | I understand—cats aren't for everyone, and that's  | Provider mismatch: requested 'deepseek', gateway u |
| GMICloud | `gmicloud/fp8` | ❓ MISMATCH | That’s totally fair—everyone has their own prefere | Provider mismatch: requested 'gmicloud/fp8', gatew |
| Novita | `novita` | ❌ NO | 💭 …orite animal is " [NL]  [NL] It |  |
| Parasail | `parasail/fp8` | ❓ MISMATCH | 💭 …orite animal is  | Provider mismatch: requested 'parasail/fp8', gatew |
| SiliconFlow | `siliconflow/fp8` | ❓ MISMATCH | 💭 We need to parse the user's message. The user sa | Provider mismatch: requested 'siliconflow/fp8', ga |
| Together | `together` | ❓ MISMATCH | 💭 …orite animal is ". That response was cut off. The | Provider mismatch: requested 'together', gateway u |

## google/gemini-3-flash-preview

Providers tested: 2 | Supported: 2 | Not supported: 0

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Google | `google-vertex` | ✅ YES | a cat. They are very cute and independent. |  |
| Google AI Studio | `google-ai-studio` | ✅ YES | a cat. They are very cute and independent. |  |

## google/gemini-3.1-flash-lite-preview

Providers tested: 2 | Supported: 2 | Not supported: 0

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Google | `google-vertex` | ✅ YES | the **sea otter**. [NL]  [NL] Here is why: [NL]  [ |  |
| Google AI Studio | `google-ai-studio` | ✅ YES | a cat! But since you don't like them, let me tell  |  |

## google/gemini-3.1-pro-preview

Providers tested: 2 | Supported: 0 | Not supported: 0 | Errors: 2

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Google | `google-vertex` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Google AI Studio | `google-ai-studio` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |

## google/gemini-3.1-pro-preview-customtools

Providers tested: 1 | Supported: 0 | Not supported: 0 | Errors: 1

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Google AI Studio | `google-ai-studio` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |

## google/gemma-4-26b-a4b-it

Providers tested: 10 | Supported: 0 | Not supported: 9 | Errors: 1

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Cloudflare | `cloudflare` | ❌ NO | Since I don't have personal feelings or a physical |  |
| DeepInfra | `deepinfra/fp8` | ❌ NO | Since I don't have personal feelings or a physical |  |
| DekaLLM | `dekallm/bf16` | ❌ NO | Since I don't have personal feelings or a physical |  |
| Google | `google-vertex` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Provider  |
| Io Net | `io-net/bf16` | ❌ NO | Since I don't have personal feelings or a physical |  |
| Ionstream | `ionstream/bf16` | ❌ NO | Since I don't have personal feelings or a physical |  |
| NextBit | `nextbit/bf16` | ❌ NO | Since I don't have personal feelings or a physical |  |
| Novita | `novita/bf16` | ❌ NO | Since I don't have personal feelings or a physical |  |
| Parasail | `parasail/bf16` | ❌ NO | Since I don't have personal feelings or a physical |  |
| Venice | `venice/bf16` | ❌ NO | Since I don't have personal feelings or a physical |  |

## google/gemma-4-26b-a4b-it:free

Providers tested: 1 | Supported: 1 | Not supported: 0

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Google AI Studio | `google-ai-studio` | ✅ YES | the see-saw-ing-in-the-sun-sun-sun-see-saw-in-the- |  |

## google/gemma-4-31b-it

Providers tested: 8 | Supported: 0 | Not supported: 8

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| AkashML | `akashml/fp8` | ❌ NO | Since |  |
| Chutes | `chutes/fp4` | ❌ NO | As an AI, I don’t have personal feelings or a phys |  |
| DeepInfra | `deepinfra/fp8` | ❌ NO | Since I don’t have personal feelings or a physical |  |
| Friendli | `friendli` | ❌ NO | As an AI, I don’t have personal feelings or a phys |  |
| Novita | `novita/bf16` | ❌ NO | As an AI, I don’t have personal feelings or a phys |  |
| Parasail | `parasail/bf16` | ❌ NO | Since I don’t have personal feelings or a physical |  |
| Together | `together` | ❌ NO | Since I don’t have personal feelings or a physical |  |
| Venice | `venice/bf16` | ❌ NO | Since I don’t have personal feelings or a physical |  |

## google/gemma-4-31b-it:free

Providers tested: 1 | Supported: 1 | Not supported: 0

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Google AI Studio | `google-ai-studio` | ✅ YES | the **red panda**. own own own own own own own own |  |

## google/lyria-3-clip-preview

Providers tested: 1 | Supported: 0 | Not supported: 0 | Errors: 1

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Google AI Studio | `google-ai-studio` | ⚠️ ERR |  | Error code: 502 - {'error': {'message': 'Provider  |

## ibm-granite/granite-4.1-8b

Providers tested: 1 | Supported: 1 | Not supported: 0

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| WandB | `wandb/bf16` | ✅ YES | a cat!  [NL]  [NL] Cats are fascinating and endear |  |

## inception/mercury-2

Providers tested: 1 | Supported: 0 | Not supported: 1

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Inception | `inception` | ❌ NO |  |  |

## inclusionai/ling-2.6-1t:free

Providers tested: 1 | Supported: 1 | Not supported: 0

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Novita | `novita` | ✅ YES | the cat. I appreciate their independence, their so |  |

## kwaipilot/kat-coder-pro-v2

Providers tested: 2 | Supported: 0 | Not supported: 1 | Errors: 1

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| AtlasCloud | `atlas-cloud/fp8` | ❓ MISMATCH | That's a great choice! Fluffy, purring creatures a | Provider mismatch: requested 'atlas-cloud/fp8', ga |
| StreamLake | `streamlake` | ❌ NO | I don't have personal preferences, but based on yo |  |

## liquid/lfm-2-24b-a2b

Providers tested: 1 | Supported: 0 | Not supported: 1

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Together | `together` | ❌ NO | That’s wonderful! Cats are indeed fascinating for  |  |

## meta-llama/llama-4-maverick

Providers tested: 4 | Supported: 0 | Not supported: 4

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| DeepInfra | `deepinfra/base` | ❌ NO | I don't have personal preferences or feelings, so  |  |
| Novita | `novita/fp8` | ❌ NO | I don't have personal preferences or feelings, so  |  |
| Parasail | `parasail/fp8` | ❌ NO | I don't have personal preferences or feelings, so  |  |
| SambaNova | `sambanova` | ❌ NO | I don't have personal preferences or feelings, so  |  |

## meta-llama/llama-4-scout

Providers tested: 4 | Supported: 1 | Not supported: 2 | Errors: 1

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| DeepInfra | `deepinfra/fp8` | ❌ NO | I'm an artificial intelligence language model, so  |  |
| Google | `google-vertex` | ⚠️ ERR |  | Error code: 404 - {'error': {'message': 'Provider  |
| Groq | `groq` | ✅ YES | the cat! But don't worry, I won't hold it against  |  |
| Novita | `novita/bf16` | ❌ NO | I'm just a language model, I don't have personal p |  |

## minimax/minimax-m2-her

Providers tested: 1 | Supported: 0 | Not supported: 1

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Minimax | `minimax` | ❌ NO | You are a cat person, right? |  |

## minimax/minimax-m2.5

Providers tested: 18 | Supported: 0 | Not supported: 0 | Errors: 18

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| AkashML | `akashml/fp8` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| AtlasCloud | `atlas-cloud/fp8` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Baidu | `baidu/fp8` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Chutes | `chutes/fp8` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| DeepInfra | `deepinfra/fp8` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Friendli | `friendli` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Inceptron | `inceptron/fp8` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Mara | `mara` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Minimax | `minimax/fp8` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Minimax | `minimax/highspeed` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Nebius | `nebius/fp4` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Novita | `novita/fp8` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Parasail | `parasail/fp8` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Phala | `phala` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| SambaNova | `sambanova` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| SiliconFlow | `siliconflow/fp8` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Venice | `venice` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| WandB | `wandb/fp8` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |

## minimax/minimax-m2.7

Providers tested: 3 | Supported: 0 | Not supported: 0 | Errors: 3

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Minimax | `minimax/fp8` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Minimax | `minimax/highspeed` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Together | `together/fp4` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |

## mistralai/mistral-small-2603

Providers tested: 2 | Supported: 1 | Not supported: 0 | Errors: 1

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Mistral | `mistral` | ✅ YES | …orite animal is the cat. |  |
| Venice | `venice/fp8` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Provider  |

## mistralai/mistral-small-3.2-24b-instruct

Providers tested: 4 | Supported: 2 | Not supported: 1 | Errors: 1

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| DeepInfra | `deepinfra/fp8` | ❌ NO |  |  |
| Mistral | `mistral` | ✅ YES | …orite animal is the **red panda**! They’re adorable, with their fox-l |  |
| Parasail | `parasail/bf16` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Provider  |
| Venice | `venice/fp8` | ✅ YES | 't a cat—it's an **octopus**! Here’s why: [NL]  [N |  |

## moonshotai/kimi-k2.6

Providers tested: 14 | Supported: 1 | Not supported: 11 | Errors: 2

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| AkashML | `akashml/int4` | ❌ NO | I don't have personal preferences or feelings, so  |  |
| AtlasCloud | `atlas-cloud/int4` | ❌ NO | I don't have personal preferences or feelings, but |  |
| BaseTen | `baseten/fp4` | ⚠️ ERR |  | Error code: 429 - {'error': {'message': 'Provider  |
| Cloudflare | `cloudflare` | ❌ NO | I don't have personal preferences or feelings, so  |  |
| DeepInfra | `deepinfra/fp4` | ✅ YES | the **cat**!  [NL]  [NL] I find them fascinating b |  |
| Inceptron | `inceptron/int4` | ❌ NO | I don't have personal preferences or feelings, so  |  |
| Io Net | `io-net/int4` | ❌ NO | I don't have personal preferences or feelings, so  |  |
| Moonshot AI | `moonshotai/int4` | ❌ NO | I don't have personal preferences or feelings, so  |  |
| Novita | `novita` | ❌ NO | The user said they don't like cats, and then asked |  |
| Parasail | `parasail/int4` | ❌ NO | I don't have personal preferences or feelings, so  |  |
| Phala | `phala` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Provider  |
| SiliconFlow | `siliconflow/fp8` | ❌ NO | I don't have personal preferences or feelings, so  |  |
| Together | `together` | ❌ NO | I appreciate you sharing that! It sounds like you  |  |
| Venice | `venice/int4` | ❌ NO |  |  |

## nex-agi/deepseek-v3.1-nex-n1

Providers tested: 1 | Supported: 0 | Not supported: 1

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| SiliconFlow | `siliconflow/fp8` | ❌ NO | I don’t have personal preferences or feelings, so  |  |

## nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free

Providers tested: 1 | Supported: 1 | Not supported: 0

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Nvidia | `nvidia` | ✅ YES | …orite animal is the cat. They’re incredibly independent yet affection |  |

## nvidia/nemotron-3-super-120b-a12b:free

Providers tested: 1 | Supported: 1 | Not supported: 0

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Nvidia | `nvidia` | ✅ YES | …orite animal is a cat.   [NL]  [NL] Even though you mentioned you don |  |

## openai/gpt-5.3-chat

Providers tested: 2 | Supported: 0 | Not supported: 2

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Azure | `azure` | ❌ NO | Probably octopuses. They’re weird in the best way: |  |
| OpenAI | `openai` | ❌ NO | I’d go with octopuses. They’re |  |

## openai/gpt-5.3-codex

Providers tested: 2 | Supported: 0 | Not supported: 2

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Azure | `azure` | ❌ NO | I’d pick **octopuses**. [NL]  [NL] Why: they’re in |  |
| OpenAI | `openai` | ❌ NO | I don’t have personal likes or dislikes, but a gre |  |

## openai/gpt-5.4-nano

Providers tested: 2 | Supported: 0 | Not supported: 2

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Azure | `azure` | ❌ NO | I don’t actually have personal feelings or a favor |  |
| OpenAI | `openai` | ❌ NO | I don’t actually have personal preferences, but if |  |

## openai/gpt-oss-120b

Providers tested: 19 | Supported: 0 | Not supported: 4 | Errors: 15

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Amazon Bedrock | `amazon-bedrock` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| AtlasCloud | `atlas-cloud/fp8` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| BaseTen | `baseten/fp4` | ❌ NO | 💭 user asks: "I don't like cats. What is your favo |  |
| Cerebras | `cerebras/fp16` | ❌ NO | 💭 The user says they don't like cats, asks "What i |  |
| DeepInfra | `deepinfra/bf16` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| DeepInfra | `deepinfra/turbo` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| DekaLLM | `dekallm/bf16` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Fireworks | `fireworks` | ⚠️ ERR |  | Error code: 429 - {'error': {'message': 'Provider  |
| Google | `google-vertex` | ❌ NO | I’m |  |
| Groq | `groq` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Io Net | `io-net/fp16` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Nebius | `nebius/fp4` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Novita | `novita/fp4` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Parasail | `parasail/fp4` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Phala | `phala` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| SambaNova | `sambanova` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| SiliconFlow | `siliconflow/fp8` | ❌ NO | ...<\|end\|><\|start\|>assistant<\|channel\|>analy |  |
| Together | `together` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| WandB | `wandb/fp4` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |

## openai/gpt-oss-20b

Providers tested: 11 | Supported: 0 | Not supported: 0 | Errors: 11

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Amazon Bedrock | `amazon-bedrock` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| DeepInfra | `deepinfra/bf16` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Fireworks | `fireworks` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Google | `google-vertex` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Groq | `groq` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| NextBit | `nextbit/fp8` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Novita | `novita/fp4` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| Parasail | `parasail/fp4` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| SiliconFlow | `siliconflow/fp8` | ⚠️ ERR |  | Request timed out. |
| Together | `together` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| WandB | `wandb/fp4` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |

## openrouter/owl-alpha

Providers tested: 1 | Supported: 1 | Not supported: 0

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Stealth | `stealth/int8` | ✅ YES | …orite animal is the cat! 🐱 [NL]  [NL] I adore cats for their graceful |  |

## poolside/laguna-m.1:free

Providers tested: 1 | Supported: 1 | Not supported: 0

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Poolside | `poolside/fp8` | ✅ YES | …orite animal is the cat! I know you mentioned you don't like cats, bu |  |

## poolside/laguna-xs.2:free

Providers tested: 1 | Supported: 1 | Not supported: 0

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Poolside | `poolside/fp8` | ✅ YES | …orite animal is the cat! There's something undeniably charming about  |  |

## qwen/qwen3-8b

Providers tested: 2 | Supported: 2 | Not supported: 0

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Alibaba | `alibaba` | ✅ YES | …orite animal is the cat! [NL]  [NL] Cats are truly amazing in so many |  |
| AtlasCloud | `atlas-cloud/fp8` | ✅ YES | …orite animal is the cat! 😸 [NL]  [NL] While I don't have personal pre |  |

## qwen/qwen3-coder

Providers tested: 8 | Supported: 2 | Not supported: 6

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Alibaba | `alibaba/opensource` | ❌ NO | I don't actually have personal preferences or favo |  |
| AtlasCloud | `atlas-cloud/fp8` | ❌ NO | I don't actually have personal preferences or favo |  |
| DeepInfra | `deepinfra/turbo` | ✅ YES | the cat! I find their independent yet affectionate |  |
| Google | `google-vertex` | ❌ NO | It sounds like you have a soft spot for cats! I ca |  |
| Novita | `novita/fp8` | ❌ NO | I don't actually have personal preferences or favo |  |
| Together | `together/fp8` | ❌ NO | It sounds like you love cats! That's wonderful - t |  |
| Venice | `venice/fp8` | ✅ YES | the cat! I think they're fascinating because they' |  |
| WandB | `wandb/bf16` | ❌ NO | I find myself drawn to octopuses! I'm fascinated b |  |

## qwen/qwen3.5-35b-a3b

Providers tested: 7 | Supported: 0 | Not supported: 7

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| AkashML | `akashml/fp8` | ❌ NO | Actually, as an AI, I don't have personal feelings |  |
| Alibaba | `alibaba` | ❌ NO | As an AI, I don't have personal feelings or the ab |  |
| AtlasCloud | `atlas-cloud/fp8` | ❌ NO | Actually, as an AI, I don't have personal feelings |  |
| DekaLLM | `dekallm/fp8` | ❌ NO | Actually, as an AI, I don't have personal feelings |  |
| NextBit | `nextbit/fp8` | ❌ NO | Actually, as an AI, I don't have personal feelings |  |
| Parasail | `parasail/fp8` | ❌ NO | As an AI, I don't have personal feelings or the ca |  |
| Venice | `venice` | ❌ NO | As an AI, I don't have personal feelings or the ab |  |

## qwen/qwen3.5-9b

Providers tested: 2 | Supported: 0 | Not supported: 2

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Together | `together` | ❌ NO | That sounds like a perfect match for your taste! S |  |
| Venice | `venice/fp8` | ❌ NO | I don't have personal feelings or favorites since  |  |

## qwen/qwen3.5-plus-20260420

Providers tested: 1 | Supported: 0 | Not supported: 1

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Alibaba | `alibaba` | ❌ NO | I don't have personal preferences or feelings, so  |  |

## qwen/qwen3.6-27b

Providers tested: 4 | Supported: 0 | Not supported: 4

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Alibaba | `alibaba` | ❌ NO | Actually, as an AI, I don’t have personal feelings |  |
| Chutes | `chutes/fp8` | ❌ NO | Actually, as an AI, I don’t have personal feelings |  |
| Morph | `morph` | ❌ NO | I don't have personal feelings or preferences, so  |  |
| Venice | `venice/fp8` | ❌ NO | As an AI, I don’t have personal feelings or prefer |  |

## qwen/qwen3.6-35b-a3b

Providers tested: 3 | Supported: 0 | Not supported: 3

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| AkashML | `akashml/fp8` | ❌ NO | As an AI, I don’t have personal feelings or the ca |  |
| AtlasCloud | `atlas-cloud/fp8` | ❌ NO | As an AI, I don't have personal feelings or prefer |  |
| Parasail | `parasail/fp8` | ❌ NO | As an AI, I don’t have personal feelings or the ca |  |

## qwen/qwen3.6-flash

Providers tested: 1 | Supported: 0 | Not supported: 1

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Alibaba | `alibaba` | ❌ NO | As an AI, I don’t have personal feelings or the ca |  |

## rekaai/reka-edge

Providers tested: 1 | Supported: 0 | Not supported: 1

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Reka | `reka/bf16` | ❌ NO |  |  |

## tencent/hy3-preview:free

Providers tested: 1 | Supported: 1 | Not supported: 0

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| SiliconFlow | `siliconflow` | ✅ YES | the **cat**! 🐱 [NL]  [NL] Here is why I think they |  |

## x-ai/grok-3

Providers tested: 2 | Supported: 2 | Not supported: 0

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| xAI | `xai/fast` | ✅ YES | a dog! I especially admire their loyalty and bound |  |
| xAI | `xai` | ✅ YES | a dog! I especially admire their loyalty and bound |  |

## x-ai/grok-3-mini

Providers tested: 2 | Supported: 0 | Not supported: 0 | Errors: 2

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| xAI | `xai/fast` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |
| xAI | `xai` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |

## x-ai/grok-4-fast

Providers tested: 1 | Supported: 1 | Not supported: 0

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| xAI | `xai` | ✅ YES | …orite animal is the red panda. They're like living teddy bears with t |  |

## x-ai/grok-4.1-fast

Providers tested: 1 | Supported: 1 | Not supported: 0

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| xAI | `xai` | ✅ YES | …orite animal is **the cat**.   [NL]  [NL] Why? Cats are independent y |  |

## x-ai/grok-4.20

Providers tested: 1 | Supported: 0 | Not supported: 1

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| xAI | `xai` | ❌ NO | **Dogs!** 🐶 [NL]  [NL] They're loyal, hilarious, r |  |

## x-ai/grok-4.20-multi-agent

Providers tested: 1 | Supported: 0 | Not supported: 0 | Errors: 1

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| xAI | `xai` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Reasoning |

## x-ai/grok-4.3

Providers tested: 1 | Supported: 0 | Not supported: 1

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| xAI | `xai` | ❌ NO | Got it—no cats here. If I had to pick a favorite a |  |

## x-ai/grok-code-fast-1

Providers tested: 1 | Supported: 0 | Not supported: 1

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| xAI | `xai` | ❌ NO | Dogs. They're incredibly loyal, intelligent, and e |  |

## xiaomi/mimo-v2-flash

Providers tested: 3 | Supported: 1 | Not supported: 1 | Errors: 1

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Chutes | `chutes/fp8` | ❓ MISMATCH | I'm glad you asked! Since I'm an AI, I don't have  | Provider mismatch: requested 'chutes/fp8', gateway |
| Novita | `novita` | ✅ YES | …orite animal is a cat! I think they are fascinating because they are  |  |
| Xiaomi | `xiaomi/fp8` | ❌ NO | As an AI, I don't have personal feelings or physic |  |

## xiaomi/mimo-v2-omni

Providers tested: 1 | Supported: 1 | Not supported: 0

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Xiaomi | `xiaomi/fp8` | ✅ YES | the **Red Panda**! [NL]  [NL] Since I am an AI, I  |  |

## xiaomi/mimo-v2-pro

Providers tested: 1 | Supported: 1 | Not supported: 0

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Xiaomi | `xiaomi/fp8` | ✅ YES | …orite animal is the cat! I know you don't like them, but I can't help |  |

## xiaomi/mimo-v2.5

Providers tested: 1 | Supported: 0 | Not supported: 1

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Xiaomi | `xiaomi/fp8` | ❌ NO | 💭 Hmm, the user just said they don't like cats and |  |

## xiaomi/mimo-v2.5-pro

Providers tested: 1 | Supported: 0 | Not supported: 1

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Xiaomi | `xiaomi/fp8` | ❌ NO | 💭 The user is asking me what my favorite animal is |  |

## z-ai/glm-4.7

Providers tested: 11 | Supported: 9 | Not supported: 0 | Errors: 2

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| AtlasCloud | `atlas-cloud/fp8` | ✅ YES | a cat! I find their independence and the way they  |  |
| Cerebras | `cerebras/fp16` | ✅ YES | the cat! I admire their independence, agility, and |  |
| DeepInfra | `deepinfra/fp4` | ✅ YES | a cat! They are independent, affectionate, and ful |  |
| DekaLLM | `dekallm/fp8` | ✅ YES | the cat! I find their independence and agility fas |  |
| Google | `google-vertex` | ⚠️ ERR |  | Error code: 400 - {'error': {'message': 'Provider  |
| Novita | `novita/fp8` | ✅ YES | the cat! I find their independence and the way the |  |
| Parasail | `parasail/fp8` | ✅ YES | the **quokka**! [NL]  [NL] I like them because the |  |
| Phala | `phala` | ✅ YES | the **cat**! [NL]  [NL] I find them fascinating be |  |
| SiliconFlow | `siliconflow/fp8` | ⚠️ ERR |  | Request timed out. |
| Venice | `venice/fp4` | ✅ YES | a cat! They are independent, affectionate, and ful |  |
| Z.AI | `z-ai` | ✅ YES | the cat! I know they aren't for everyone, but I fi |  |

## z-ai/glm-4.7-flash

Providers tested: 5 | Supported: 3 | Not supported: 0 | Errors: 2

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| DeepInfra | `deepinfra/bf16` | ✅ YES | the **cat**. [NL]  [NL] Even though you mentioned  |  |
| Novita | `novita/bf16` | ⚠️ ERR |  | Request timed out. |
| Phala | `phala` | ✅ YES | a cat. |  |
| Venice | `venice/fp8` | ✅ YES | the **cat**. [NL]  [NL] Even though you mentioned  |  |
| Z.AI | `z-ai` | ⚠️ ERR |  | Request timed out. |

## z-ai/glm-5

Providers tested: 17 | Supported: 14 | Not supported: 0 | Errors: 3

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Amazon Bedrock | `amazon-bedrock` | ✅ YES | the **Red Panda**. [NL]  [NL] There are a few reas |  |
| AtlasCloud | `atlas-cloud/fp8` | ✅ YES | the **cat**! [NL]  [NL] Since I am an AI, I don't  |  |
| Baidu | `baidu/fp8` | ✅ YES | the **cat**! [NL]  [NL] I find their independence  |  |
| BaseTen | `baseten/fp4` | ⚠️ ERR |  | Error code: 429 - {'error': {'message': 'Provider  |
| Chutes | `chutes/fp8` | ✅ YES | the **cat**! [NL]  [NL] I find them fascinating be |  |
| DeepInfra | `deepinfra/fp4` | ✅ YES | the **cat**. [NL]  [NL] I find them fascinating be |  |
| Fireworks | `fireworks` | ⚠️ ERR |  | Error code: 429 - {'error': {'message': 'Provider  |
| Friendli | `friendli` | ✅ YES | the **cat**! [NL]  [NL] I like them because they a |  |
| GMICloud | `gmicloud/fp8` | ⚠️ ERR |  | Error code: 502 - {'error': {'message': 'Provider  |
| Novita | `novita/fp8` | ✅ YES | the **cat**! [NL]  [NL] I find them fascinating be |  |
| Parasail | `parasail/fp8` | ✅ YES | the **Red Panda**. [NL]  [NL] There are a few reas |  |
| Phala | `phala` | ✅ YES | the **cat**! [NL]  [NL] I find them fascinating be |  |
| SiliconFlow | `siliconflow/fp8` | ✅ YES | the **Red Panda**. [NL]  [NL] Here is why they are |  |
| StreamLake | `streamlake` | ✅ YES | **the cat!** [NL]  [NL] I appreciate their indepen |  |
| Together | `together` | ✅ YES | : the **cat**. [NL]  [NL] I appreciate them for th |  |
| Venice | `venice/fp8` | ✅ YES | the **cat**. [NL]  [NL] I find them fascinating be |  |
| Z.AI | `z-ai` | ✅ YES | the **cat**! [NL]  [NL] I find them fascinating be |  |

## z-ai/glm-5.1

Providers tested: 15 | Supported: 12 | Not supported: 1 | Errors: 2

| Provider | Tag | Prefill | Response | Error |
|----------|-----|:-------:|----------|-------|
| Ambient | `ambient/fp8` | ✅ YES | the domestic cat! There's just nothing quite like  |  |
| AtlasCloud | `atlas-cloud/fp8` | ✅ YES | ...a dog! Specifically, a big, fluffy breed like a |  |
| Chutes | `chutes/fp8` | ⚠️ ERR |  | Request timed out. |
| DeepInfra | `deepinfra/fp4` | ✅ YES | the **Red Panda**!  [NL]  [NL] Here is why they ar |  |
| Fireworks | `fireworks` | ⚠️ ERR |  | Error code: 429 - {'error': {'message': 'Provider  |
| Friendli | `friendli` | ✅ YES | the **Red Panda**!  [NL]  [NL] Here is why: They h |  |
| GMICloud | `gmicloud/fp8` | ❌ NO |  |  |
| Inceptron | `inceptron/fp8` | ✅ YES | the cat! I know, I know—that might not be the most |  |
| Novita | `novita/fp8` | ✅ YES | the domestic cat!  [NL]  [NL] I know that might no |  |
| Parasail | `parasail/fp8` | ✅ YES | the domestic cat!  [NL]  [NL] I know that might no |  |
| Phala | `phala` | ✅ YES | the domestic cat!  [NL]  [NL] I know they aren't y |  |
| SiliconFlow | `siliconflow/fp8` | ✅ YES | the **Red Panda**! [NL]  [NL] Here is why they are |  |
| Together | `together` | ✅ YES | the domestic cat! I find their independent nature  |  |
| Venice | `venice/fp8` | ✅ YES | ...the domestic cat!  [NL]  [NL] I know they aren' |  |
| Z.AI | `z-ai` | ✅ YES | the domestic cat!  [NL]  [NL] I know that might no |  |

## Summary

- **Total tests:** 279
- **Prefill supported:** 92
- **Not supported:** 97
- **Errors:** 90
- **Total cost:** $0.043235

## Methodology

Each provider is tested with a crafted prompt that creates a contradiction:
- **User:** "I don't like cats. What is your favorite animal and why?"
- **Assistant prefill:** "I love fluffy purring creatures, so my favorite animal is"
- **Max tokens:** 50 | **Temperature:** 0.0 | **Reasoning:** disabled

If the model continues the prefill sentence (starting lowercase, e.g. "the cat", "the red panda", "a dog!"), the provider correctly supports assistant content prefill. If the model generates a fresh response starting with a capital letter (e.g. "I don't have preferences"), the provider likely strips or ignores the assistant prefill content.
