"""Runner: tests assistant prefill support for a single (model, provider) pair.

Sends a crafted prompt where the user dislikes cats, but the assistant
prefill loves them.  If the model continues the prefill sentence (with
any animal, not just "cat"), the provider supports prefill.

Detects provider routing mismatches (gateway ignoring provider constraints)
and flags reasoning leaks (model reasoning despite reasoning.enabled=false).
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from prefill_bench.config import (
    ASSISTANT_PREFILL,
    CACHE_DIR,
    PREFILL_MAX_TOKENS,
    PREFILL_TEMPERATURE,
    USER_PROMPT,
    ProviderEndpoint,
    TestResult,
    model_id_to_slug,
)
from prefill_bench.openrouter_client import (
    OpenRouterClient,
    ProviderMismatchError,
    _providers_match,
)

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
        "response_text": result.response_text,
        "prefill_supported": result.prefill_supported,
        "model_id": result.model_id,
        "provider_name": result.provider_name,
        "provider_tag": result.provider_tag,
        "resolved_provider": result.resolved_provider,
        "provider_mismatch": result.provider_mismatch,
        "error": result.error,
        "prompt_tokens": result.prompt_tokens,
        "completion_tokens": result.completion_tokens,
        "reasoning_tokens": result.reasoning_tokens,
        "reasoning_content": result.reasoning_content,
        "cost_usd": round(result.cost_usd, 8),
        "elapsed_seconds": round(result.elapsed_seconds, 3),
        "http_status": result.http_status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path


def check_prefill_response(
    response_text: str,
    reasoning_content: str | None = None,
) -> bool:
    """Determine if the provider delivered the assistant prefill.

    The check does NOT look for a specific keyword (e.g. "cat").  Instead
    it detects structural signs that the response is a *continuation* of
    the prefill sentence rather than a fresh model turn.

    1. If the response contains the full prefill text, the provider
       echoed it back — prefill is supported.  For reasoning content,
       only match when the prefill appears at the very start — models
       often *quote* the prefill mid-reasoning while analyzing the
       conversation, which does not prove the provider delivered it.
    2. Strip inline markdown emphasis (``*``/``**``) and leading
       ellipsis/punctuation, then check whether the first character is a
       lowercase letter, an apostrophe (contraction like ``'t a cat``),
       or a colon.  A continuation of "my favorite animal is" naturally
       starts lowercase (``the red panda``, ``a dog!``), while a fresh
       response starts with uppercase (``I don't have preferences``,
       ``That's a great question``).  Applied to ``response_text`` only
       — reasoning content is internal monologue, not a continuation.
    3. If "kidding" or "joke" appears in the first four words the model
       is reacting to the prefill contradiction — mark as supported.
    """
    prefill_lower = ASSISTANT_PREFILL.lower()

    if response_text and prefill_lower in response_text.lower():
        return True

    if reasoning_content and reasoning_content.lower().startswith(prefill_lower):
        return True

    if response_text:
        stripped = _strip_continuation_prefix(response_text)
        if stripped:
            ch = stripped[0]
            if ch.islower() or ch in ("'", "\u2019", ":"):
                return True

        first4 = " ".join(response_text.split()[:4]).lower()
        if "kidding" in first4 or "joke" in first4:
            return True

    return False


def _strip_continuation_prefix(text: str) -> str:
    """Strip leading markdown emphasis and ellipsis so we can inspect the
    first meaningful character of a potential prefill continuation."""
    import re

    s = text.lstrip()
    s = re.sub(r"^\*{1,2}", "", s).lstrip()
    if s.startswith("..."):
        s = s[3:].lstrip()
    elif s.startswith("\u2026"):
        s = s[1:].lstrip()
    s = re.sub(r"^\*{1,2}", "", s).lstrip()
    return s


def _verify_provider(
    provider_tag: str,
    resolved_provider: str | None,
    model_id: str,
) -> str | None:
    """Check that the gateway actually used the configured provider.

    Returns an error message if mismatched, None if OK or unknown.
    """
    if not resolved_provider:
        return None

    if _providers_match(provider_tag, resolved_provider):
        return None

    return (
        f"Provider mismatch: requested '{provider_tag}', "
        f"gateway used '{resolved_provider}'. Result invalid."
    )


def test_provider(
    client: OpenRouterClient,
    model_id: str,
    provider: ProviderEndpoint,
    *,
    force: bool = False,
    reasoning: dict[str, Any] | None = None,
    include_reasoning: bool | None = None,
    allow_reasoning: bool = False,
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
            result.reasoning_tokens = cached.get("reasoning_tokens", 0)
            result.reasoning_content = cached.get("reasoning_content")
            result.cost_usd = cached.get("cost_usd", 0.0)
            result.http_status = cached.get("http_status")
            result.resolved_provider = cached.get("resolved_provider")
            result.provider_mismatch = cached.get("provider_mismatch")
            return result

    chat_result = client.chat_with_prefill(
        model=model_id,
        user_message=USER_PROMPT,
        assistant_prefill=ASSISTANT_PREFILL,
        max_tokens=PREFILL_MAX_TOKENS,
        temperature=PREFILL_TEMPERATURE,
        provider_tag=provider.tag,
        reasoning=reasoning,
        include_reasoning=include_reasoning,
        allow_reasoning=allow_reasoning,
    )

    result.response_text = chat_result["content"]
    result.elapsed_seconds = chat_result["elapsed"]
    result.prompt_tokens = chat_result["prompt_tokens"]
    result.completion_tokens = chat_result["completion_tokens"]
    result.reasoning_tokens = chat_result["reasoning_tokens"]
    result.reasoning_content = chat_result["reasoning_content"]
    result.cost_usd = chat_result["cost_usd"]
    result.http_status = chat_result["http_status"]
    result.error = chat_result["error"]
    result.resolved_provider = chat_result["resolved_provider"]

    # Provider mismatch detection
    mismatch_msg = _verify_provider(
        provider.tag, result.resolved_provider, model_id,
    )
    if mismatch_msg:
        result.provider_mismatch = mismatch_msg
        result.prefill_supported = None
        result.error = mismatch_msg
    elif result.error:
        result.prefill_supported = None
    else:
        result.prefill_supported = check_prefill_response(
            result.response_text, result.reasoning_content,
        )

    save_result(model_id, provider.tag, result)
    return result
