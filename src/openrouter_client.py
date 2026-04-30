"""OpenRouter client for the prefill support matrix benchmark.

Discovery (models list, provider endpoints) calls OpenRouter directly
— no authentication required for these public endpoints.

Chat completions go through the local proxy with the proxy key.
"""

from __future__ import annotations

import logging
import time
from typing import Any

import httpx
import requests
from openai import OpenAI

from src.config import (
    API_CALL_TIMEOUT,
    OPENROUTER_API_URL,
    OPENROUTER_MODELS_URL,
    PROXY_BASE_URL,
    ProviderEndpoint,
)

log = logging.getLogger(__name__)


class ProviderMismatchError(RuntimeError):
    """Raised when the gateway routed the request to a different provider."""

    def __init__(self, expected: str, actual: str, model: str) -> None:
        self.expected = expected
        self.actual = actual
        self.model = model
        super().__init__(
            f"Provider mismatch for {model}: expected '{expected}', "
            f"gateway resolved to '{actual}'."
        )


def _to_plain_object(value: Any) -> Any:
    """Recursively convert SDK objects to plain dicts/lists."""
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if isinstance(value, dict):
        return {k: _to_plain_object(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_to_plain_object(item) for item in value]
    if hasattr(value, "__dict__"):
        return {
            k: _to_plain_object(v)
            for k, v in value.__dict__.items()
            if not k.startswith("_")
        }
    return value


def _extract_resolved_provider(response: Any) -> str | None:
    """Extract the actual provider from the response.

    OpenRouter returns a top-level ``provider`` field. Our proxy may
    also embed routing info under
    ``choices[].message.provider_metadata.gateway.routing.finalProvider``.
    """
    top_level = getattr(response, "provider", None)
    if isinstance(top_level, str) and top_level.strip():
        return top_level.strip()

    choices = getattr(response, "choices", None) or []
    if not choices:
        return None
    message = getattr(choices[0], "message", None)
    if message is None:
        return None

    pm = getattr(message, "provider_metadata", None)
    if pm is None:
        raw = _to_plain_object(message)
        pm = raw.get("provider_metadata") if isinstance(raw, dict) else None
    else:
        pm = _to_plain_object(pm)

    if not isinstance(pm, dict):
        return None
    gateway = pm.get("gateway")
    if not isinstance(gateway, dict):
        return None
    routing = gateway.get("routing")
    if not isinstance(routing, dict):
        return None
    final = routing.get("finalProvider")
    if isinstance(final, str) and final.strip():
        return final.strip()
    return None


def _normalize_provider_name(name: str) -> str:
    """Normalize a provider name/tag for comparison.

    Strips quantization suffixes (``/fp8``, ``/bf16``, ``/turbo``, etc.),
    removes hyphens/underscores, and lowercases.
    """
    s = name.lower().strip()
    # Strip quantization / variant suffix: atlas-cloud/fp8 -> atlas-cloud
    if "/" in s:
        s = s.split("/")[0]
    return s.replace("-", "").replace("_", "").replace(" ", "")


def _providers_match(configured: str, resolved: str) -> bool:
    """Case-insensitive comparison with normalization and alias handling.

    The ``configured`` value is typically a provider tag like ``atlas-cloud/fp8``
    and ``resolved`` is a provider name like ``AtlasCloud``.
    """
    c = _normalize_provider_name(configured)
    r = _normalize_provider_name(resolved)
    if c == r:
        return True
    if c in r or r in c:
        return True
    ALIASES: dict[str, set[str]] = {
        "amazonbedrock": {"bedrock", "amazonbedrock", "awsbedrock"},
        "googleaistudio": {"google", "googleaistudio", "googlevertex"},
        "moonshotai": {"moonshot", "moonshotai"},
    }
    for _canonical, aliases in ALIASES.items():
        group = aliases | {_canonical}
        if c in group and r in group:
            return True
    return False


def _is_reasoning_param_error(status_code: int | None, error_msg: str) -> bool:
    """Detect 400 errors caused by unsupported/invalid reasoning payloads."""
    if status_code != 400:
        return False
    if "reasoning" not in error_msg:
        return False

    incompatible_markers = (
        "invalid",
        "unsupported",
        "unknown",
        "not allowed",
        "not supported",
        "schema",
        "enum",
        "bad request",
    )
    return any(marker in error_msg for marker in incompatible_markers)


def _reasoning_requests_disable(reasoning_cfg: dict[str, Any]) -> bool:
    """Return True when reasoning config attempts to disable reasoning."""
    effort = reasoning_cfg.get("effort")
    if isinstance(effort, str) and effort.strip().lower() == "none":
        return True

    enabled = reasoning_cfg.get("enabled")
    if enabled is False:
        return True

    max_tokens = reasoning_cfg.get("max_tokens")
    if isinstance(max_tokens, (int, float)) and not isinstance(max_tokens, bool):
        if max_tokens <= 0:
            return True

    return False


def _build_full_reasoning_suppression(
    reasoning: dict[str, Any] | None,
) -> dict[str, Any] | None:
    """Build a comprehensive reasoning suppression payload.

    When the caller provides a reasoning config that attempts to disable
    reasoning (effort=none, enabled=false, max_tokens=0, or exclude=true),
    we merge ALL known suppression mechanisms so every provider variant
    gets the signal it understands:

      effort=none   — OpenAI / Minimax style
      max_tokens=0  — token-budget style
      exclude=true  — OpenRouter exclusion flag

    If the config doesn't attempt to suppress reasoning (or is None),
    returns None so no reasoning field is sent.
    """
    if reasoning is None:
        return None

    if not _reasoning_requests_disable(reasoning) and not reasoning.get("exclude"):
        return dict(reasoning)

    return {
        **reasoning,
        "effort": reasoning.get("effort", "none"),
        "max_tokens": reasoning.get("max_tokens", 0),
        "exclude": True,
    }


def _extract_reasoning_content(msg: Any) -> str | None:
    """Extract reasoning text from a completion message."""
    raw = getattr(msg, "reasoning", None)
    if raw and isinstance(raw, str):
        return raw.strip()

    raw = getattr(msg, "reasoning_content", None)
    if raw and isinstance(raw, str):
        return raw.strip()

    details = getattr(msg, "reasoning_details", None)
    if details and isinstance(details, list):
        text_parts: list[str] = []
        for item in details:
            if not isinstance(item, dict):
                continue
            if item.get("type") == "reasoning.text" and item.get("text"):
                text_parts.append(item["text"])
        if text_parts:
            return "\n".join(text_parts).strip()

    return None


def _extract_cost(usage_obj: Any) -> float:
    """Extract cost from usage, falling back to market_cost for byok proxies."""
    raw_cost = getattr(usage_obj, "cost", None)
    if isinstance(raw_cost, (int, float)) and not isinstance(raw_cost, bool) and raw_cost > 0:
        return float(raw_cost)

    if isinstance(raw_cost, str) and raw_cost.strip():
        try:
            val = float(raw_cost)
            if val > 0:
                return val
        except ValueError:
            pass

    market_cost = getattr(usage_obj, "market_cost", None)
    if isinstance(market_cost, (int, float)) and not isinstance(market_cost, bool) and market_cost > 0:
        return float(market_cost)

    if isinstance(market_cost, str) and market_cost.strip():
        try:
            val = float(market_cost)
            if val > 0:
                return val
        except ValueError:
            pass

    return 0.0


def _extract_reasoning_tokens(usage_obj: Any) -> int:
    """Extract reasoning token count from completion_tokens_details."""
    details = getattr(usage_obj, "completion_tokens_details", None)
    if details:
        rt = getattr(details, "reasoning_tokens", None)
        if rt is not None:
            return int(rt)
    return 0


class OpenRouterClient:
    MAX_RETRIES = 2
    RETRY_BACKOFF_BASE = 2.0
    RETRYABLE_STATUS_CODES = {429, 500, 502, 503}

    def __init__(self, api_key: str, timeout: float = API_CALL_TIMEOUT) -> None:
        self.api_key = api_key
        self._client = OpenAI(
            base_url=PROXY_BASE_URL,
            api_key=api_key,
            timeout=httpx.Timeout(timeout, connect=10.0),
        )
        self._models_cache: dict[str, Any] | None = None

    def _fetch_models_raw(self) -> list[dict[str, Any]]:
        """Fetch models from OpenRouter directly (no auth needed)."""
        if self._models_cache is not None:
            return self._models_cache  # type: ignore[return-value]
        resp = requests.get(OPENROUTER_MODELS_URL, timeout=30)
        resp.raise_for_status()
        data = resp.json().get("data", [])
        self._models_cache = data
        return data

    def get_canonical_slug(self, model_id: str) -> str | None:
        """Get the canonical_slug for a model (needed for endpoints API)."""
        models = self._fetch_models_raw()
        for m in models:
            if m.get("id") == model_id:
                return m.get("canonical_slug") or model_id
        return None

    def validate_model(self, model_id: str) -> bool:
        models = self._fetch_models_raw()
        return any(m.get("id") == model_id for m in models)

    def fetch_providers(self, model_id: str) -> list[ProviderEndpoint]:
        """Fetch all provider endpoints for a given model from OpenRouter."""
        canonical = self.get_canonical_slug(model_id)
        if not canonical:
            log.warning("Model %s not found in OpenRouter catalog", model_id)
            return []

        # Important: model variants (especially :free) can have a different
        # provider set than the canonical slug. Query by the exact model id first.
        slugs_to_try = [model_id]
        if canonical != model_id:
            slugs_to_try.append(canonical)

        endpoints: list[dict[str, Any]] = []
        for slug in slugs_to_try:
            url = f"{OPENROUTER_API_URL}/models/{slug}/endpoints"
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            raw = resp.json().get("data", {})
            eps = raw.get("endpoints", [])
            if eps:
                endpoints = eps
                break

        providers: list[ProviderEndpoint] = []
        for ep in endpoints:
            tag = ep.get("tag", "")
            if not tag:
                continue
            pricing = ep.get("pricing", {})
            providers.append(ProviderEndpoint(
                provider_name=ep.get("provider_name", tag),
                tag=tag,
                quantization=ep.get("quantization", "unknown"),
                context_length=ep.get("context_length", 0),
                max_completion_tokens=ep.get("max_completion_tokens"),
                pricing_prompt=float(pricing.get("prompt", "0")),
                pricing_completion=float(pricing.get("completion", "0")),
                supported_parameters=ep.get("supported_parameters", []),
            ))

        return providers

    def chat_with_prefill(
        self,
        model: str,
        user_message: str,
        assistant_prefill: str,
        max_tokens: int = 50,
        temperature: float = 0.0,
        *,
        provider_tag: str | None = None,
        reasoning: dict[str, Any] | None = None,
        include_reasoning: bool | None = None,
    ) -> dict[str, Any]:
        """Send a chat completion with an assistant prefill message.

        Key extra-body parameters:

        * ``continue_final_message: true`` — tells vLLM-backed providers
          to continue the assistant message instead of treating it as a
          completed turn.  Non-vLLM providers silently ignore it.
        * ``reasoning`` — optional model-specific reasoning config from
          benchmark config. When reasoning suppression is requested, we
          send ALL known suppression mechanisms simultaneously:
          ``effort=none``, ``max_tokens=0``, ``exclude=true``, and
          ``include_reasoning=false``.  If a provider rejects reasoning
          parameters or requires mandatory reasoning, we retry without.
        * ``include_reasoning`` — legacy flag that works alongside the
          ``reasoning`` object for maximum compatibility.

        Reasoning tokens and content are always captured so leaks can be
        detected and reported.
        """
        messages: list[dict[str, str]] = [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": assistant_prefill},
        ]

        result: dict[str, Any] = {
            "content": "",
            "elapsed": 0.0,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "reasoning_tokens": 0,
            "reasoning_content": None,
            "cost_usd": 0.0,
            "finish_reason": "",
            "http_status": None,
            "resolved_provider": None,
            "error": "",
        }

        current_reasoning = _build_full_reasoning_suppression(reasoning)
        if current_reasoning is None and include_reasoning is False:
            current_reasoning = _build_full_reasoning_suppression({"exclude": True})
        include_reasoning_control = current_reasoning is not None
        effective_include_reasoning = include_reasoning
        if include_reasoning_control and effective_include_reasoning is None:
            effective_include_reasoning = False
        last_error: Exception | None = None
        for attempt in range(self.MAX_RETRIES + 1):
            try:
                extra_body: dict[str, Any] = {
                    "continue_final_message": True,
                }
                if include_reasoning_control:
                    extra_body["reasoning"] = dict(current_reasoning or {})
                if effective_include_reasoning is not None:
                    extra_body["include_reasoning"] = effective_include_reasoning
                if provider_tag:
                    extra_body["provider"] = {
                        "order": [provider_tag],
                        "allow_fallbacks": False,
                    }

                kwargs: dict[str, Any] = {
                    "model": model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                }
                if extra_body:
                    kwargs["extra_body"] = extra_body

                t0 = time.monotonic()
                response = self._client.chat.completions.create(**kwargs)
                elapsed = time.monotonic() - t0

                result["elapsed"] = elapsed
                result["http_status"] = 200

                if response.usage:
                    result["prompt_tokens"] = int(response.usage.prompt_tokens or 0)
                    result["completion_tokens"] = int(response.usage.completion_tokens or 0)
                    result["reasoning_tokens"] = _extract_reasoning_tokens(response.usage)
                    result["cost_usd"] = _extract_cost(response.usage)

                result["resolved_provider"] = _extract_resolved_provider(response)

                if response.choices:
                    result["finish_reason"] = response.choices[0].finish_reason or ""
                    content = response.choices[0].message.content
                    if content:
                        result["content"] = content.strip()

                    result["reasoning_content"] = _extract_reasoning_content(
                        response.choices[0].message
                    )

                return result

            except Exception as e:
                last_error = e
                status_code = getattr(e, "status_code", None)
                result["http_status"] = status_code
                error_msg = str(e).lower()

                if (
                    include_reasoning_control
                    and status_code == 400
                    and "reasoning is mandatory" in error_msg
                ):
                    if current_reasoning and _reasoning_requests_disable(current_reasoning):
                        current_reasoning = {"exclude": True}
                        log.info(
                            "Model %s requires reasoning; retrying with reasoning.exclude=true",
                            model,
                        )
                    else:
                        include_reasoning_control = False
                        log.info(
                            "Model %s requires reasoning, retrying without reasoning field",
                            model,
                        )
                    continue
                if include_reasoning_control and _is_reasoning_param_error(status_code, error_msg):
                    include_reasoning_control = False
                    effective_include_reasoning = None
                    log.info(
                        "Provider rejected reasoning controls for %s, retrying without reasoning field",
                        model,
                    )
                    continue

                if status_code and status_code in self.RETRYABLE_STATUS_CODES:
                    if attempt < self.MAX_RETRIES:
                        wait = self.RETRY_BACKOFF_BASE ** (attempt + 1)
                        time.sleep(wait)
                        continue

                result["error"] = str(e)
                return result

        if last_error:
            result["error"] = str(last_error)
        return result
