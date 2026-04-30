"""Runner: tests assistant prefill support for a single (model, provider) pair.

Sends a crafted prompt where the user dislikes cats, but the assistant
prefill loves them. If the model continues with "cat" (within max_tokens=3),
the prefill is working. If not, the provider likely stripped/ignored it.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.config import (
    ASSISTANT_PREFILL,
    CACHE_DIR,
    EXPECTED_KEYWORD,
    PREFILL_MAX_TOKENS,
    PREFILL_TEMPERATURE,
    USER_PROMPT,
    ProviderEndpoint,
    TestResult,
    model_id_to_slug,
)
from src.openrouter_client import OpenRouterClient

log = logging.getLogger(__name__)


def _cache_path(model_id: str, provider_tag: str) -> Path:
    slug = model_id_to_slug(model_id)
    provider_slug = provider_tag.replace("/", "-")
    return CACHE_DIR / slug / f"{provider_slug}.json"


def load_cached_result(model_id: str, provider_tag: str) -> dict[str, Any] | None:
    path = _cache_path(model_id, provider_tag)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def save_result(model_id: str, provider_tag: str, result: TestResult) -> Path:
    path = _cache_path(model_id, provider_tag)
    path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "model_id": result.model_id,
        "provider_name": result.provider_name,
        "provider_tag": result.provider_tag,
        "prefill_supported": result.prefill_supported,
        "response_text": result.response_text,
        "error": result.error,
        "elapsed_seconds": round(result.elapsed_seconds, 3),
        "prompt_tokens": result.prompt_tokens,
        "completion_tokens": result.completion_tokens,
        "cost_usd": round(result.cost_usd, 8),
        "http_status": result.http_status,
        "test_params": {
            "user_prompt": USER_PROMPT,
            "assistant_prefill": ASSISTANT_PREFILL,
            "expected_keyword": EXPECTED_KEYWORD,
            "max_tokens": PREFILL_MAX_TOKENS,
            "temperature": PREFILL_TEMPERATURE,
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path


def check_prefill_response(response_text: str) -> bool:
    """Determine if the prefill worked by checking for the expected keyword."""
    if not response_text:
        return False
    return EXPECTED_KEYWORD in response_text.lower()


def test_provider(
    client: OpenRouterClient,
    model_id: str,
    provider: ProviderEndpoint,
    *,
    force: bool = False,
) -> TestResult:
    """Run the prefill test for a single (model, provider) pair.

    Returns cached results unless force=True.
    """
    result = TestResult(
        model_id=model_id,
        provider_name=provider.provider_name,
        provider_tag=provider.tag,
    )

    if not force:
        cached = load_cached_result(model_id, provider.tag)
        if cached is not None:
            result.prefill_supported = cached.get("prefill_supported")
            result.response_text = cached.get("response_text", "")
            result.error = cached.get("error", "")
            result.elapsed_seconds = cached.get("elapsed_seconds", 0.0)
            result.prompt_tokens = cached.get("prompt_tokens", 0)
            result.completion_tokens = cached.get("completion_tokens", 0)
            result.cost_usd = cached.get("cost_usd", 0.0)
            result.http_status = cached.get("http_status")
            return result

    chat_result = client.chat_with_prefill(
        model=model_id,
        user_message=USER_PROMPT,
        assistant_prefill=ASSISTANT_PREFILL,
        max_tokens=PREFILL_MAX_TOKENS,
        temperature=PREFILL_TEMPERATURE,
        provider_tag=provider.tag,
    )

    result.response_text = chat_result["content"]
    result.elapsed_seconds = chat_result["elapsed"]
    result.prompt_tokens = chat_result["prompt_tokens"]
    result.completion_tokens = chat_result["completion_tokens"]
    result.cost_usd = chat_result["cost_usd"]
    result.http_status = chat_result["http_status"]
    result.error = chat_result["error"]

    if result.error:
        result.prefill_supported = None
    else:
        result.prefill_supported = check_prefill_response(result.response_text)

    save_result(model_id, provider.tag, result)
    return result
