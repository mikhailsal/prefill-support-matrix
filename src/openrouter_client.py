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

        url = f"{OPENROUTER_API_URL}/models/{canonical}/endpoints"
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()

        raw = resp.json().get("data", {})
        endpoints = raw.get("endpoints", [])

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
        max_tokens: int = 3,
        temperature: float = 0.0,
        *,
        provider_tag: str | None = None,
    ) -> dict[str, Any]:
        """Send a chat completion with an assistant prefill message.

        Returns a dict with: content, elapsed, prompt_tokens, completion_tokens,
        cost_usd, finish_reason, http_status, error.
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
            "cost_usd": 0.0,
            "finish_reason": "",
            "http_status": None,
            "error": "",
        }

        last_error: Exception | None = None
        for attempt in range(self.MAX_RETRIES + 1):
            try:
                extra_body: dict[str, Any] = {}
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
                    raw_cost = getattr(response.usage, "cost", None)
                    if raw_cost is not None:
                        try:
                            result["cost_usd"] = float(raw_cost)
                        except (ValueError, TypeError):
                            pass

                if response.choices:
                    result["finish_reason"] = response.choices[0].finish_reason or ""
                    content = response.choices[0].message.content
                    if content:
                        result["content"] = content.strip()

                return result

            except Exception as e:
                last_error = e
                status_code = getattr(e, "status_code", None)
                result["http_status"] = status_code

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
