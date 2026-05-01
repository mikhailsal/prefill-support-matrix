"""Configuration for the Prefill Support Matrix benchmark.

Tests assistant content prefill support across OpenRouter providers.

Discovery (models/endpoints) goes to OpenRouter directly — no auth needed.
Chat completions go through the local proxy with the proxy key.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = PROJECT_ROOT / "cache"
RESULTS_DIR = PROJECT_ROOT / "results"
COST_LOG_PATH = RESULTS_DIR / "cost_log.json"
ENV_PATH = PROJECT_ROOT / ".env"
CONFIGS_PATH = PROJECT_ROOT / "configs" / "models.yaml"

# ---------------------------------------------------------------------------
# OpenRouter — discovery endpoints (no auth required)
# ---------------------------------------------------------------------------
OPENROUTER_API_URL = "https://openrouter.ai/api/v1"
OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"

# ---------------------------------------------------------------------------
# Proxy — chat completions go through the local proxy
# ---------------------------------------------------------------------------
PROXY_BASE_URL = "http://localhost:8000/v1"
API_CALL_TIMEOUT = 30

# ---------------------------------------------------------------------------
# Prefill test parameters
# ---------------------------------------------------------------------------
PREFILL_MAX_TOKENS = 50
PREFILL_TEMPERATURE = 0.0

USER_PROMPT = "I don't like cats. What is your favorite animal and why?"
ASSISTANT_PREFILL = "I love fluffy purring creatures, so my favorite animal is"
EXPECTED_KEYWORD = "cat"

# ---------------------------------------------------------------------------
# Concurrency
# ---------------------------------------------------------------------------
DEFAULT_PARALLEL = 16


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ProviderEndpoint:
    """A single provider endpoint for a model on OpenRouter."""
    provider_name: str
    tag: str
    quantization: str
    context_length: int
    max_completion_tokens: int | None
    pricing_prompt: float
    pricing_completion: float
    supported_parameters: list[str] = field(default_factory=list)

    @property
    def slug(self) -> str:
        return self.tag


@dataclass
class TestResult:
    """Result of a single prefill test for one (model, provider) pair."""
    model_id: str
    provider_name: str
    provider_tag: str
    prefill_supported: bool | None = None  # None = error/unknown
    response_text: str = ""
    error: str = ""
    elapsed_seconds: float = 0.0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    reasoning_tokens: int = 0
    reasoning_content: str | None = None
    cost_usd: float = 0.0
    http_status: int | None = None
    resolved_provider: str | None = None
    provider_mismatch: str | None = None


@dataclass(frozen=True)
class ModelTarget:
    """Model configuration for benchmark execution."""
    model_id: str
    reasoning: dict[str, Any] | None = None
    include_reasoning: bool | None = None
    allow_reasoning: bool = False


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def model_id_to_slug(model_id: str) -> str:
    return model_id.replace("/", "--")


def ensure_dirs() -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def load_api_key() -> str:
    load_dotenv(ENV_PATH)
    key = os.environ.get("OPENROUTER_KEY", "").strip()
    if not key:
        key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key or key == "your-key-here":
        print(
            "ERROR: OPENROUTER_KEY is not set.\n"
            f"  Create a .env file at {ENV_PATH} with:\n"
            "  OPENROUTER_KEY=sk-or-...\n"
            "  Or export it as an environment variable.",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def load_provider_aliases(path: Path | None = None) -> dict[str, list[str]]:
    """Load provider_aliases from YAML config.

    Returns a mapping of canonical provider name to a list of alternative
    names that should be treated as equivalent during mismatch detection.
    """
    import yaml

    config_path = path or CONFIGS_PATH
    if not config_path.exists():
        return {}

    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if not data:
        return {}

    raw = data.get("provider_aliases", {})
    if not isinstance(raw, dict):
        return {}

    result: dict[str, list[str]] = {}
    for canonical, alternatives in raw.items():
        if isinstance(alternatives, list):
            result[str(canonical)] = [str(a) for a in alternatives]
        elif isinstance(alternatives, str):
            result[str(canonical)] = [alternatives]
    return result


def load_model_targets(path: Path | None = None) -> list[ModelTarget]:
    """Load model targets and optional reasoning config from YAML."""
    import yaml

    config_path = path or CONFIGS_PATH
    if not config_path.exists():
        return []

    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if not data or "models" not in data:
        return []

    targets: list[ModelTarget] = []
    for raw in data["models"]:
        if not raw:
            continue

        if isinstance(raw, str):
            targets.append(ModelTarget(model_id=raw))
            continue

        if isinstance(raw, dict):
            model_id = str(raw.get("id") or raw.get("model") or "").strip()
            if not model_id:
                continue
            reasoning_raw = raw.get("reasoning")
            reasoning_cfg = reasoning_raw if isinstance(reasoning_raw, dict) else None
            include_reasoning_raw = raw.get("include_reasoning")
            include_reasoning_cfg = (
                include_reasoning_raw
                if isinstance(include_reasoning_raw, bool)
                else None
            )
            allow_reasoning_raw = raw.get("allow_reasoning")
            allow_reasoning_cfg = (
                allow_reasoning_raw is True
            )
            targets.append(
                ModelTarget(
                    model_id=model_id,
                    reasoning=reasoning_cfg,
                    include_reasoning=include_reasoning_cfg,
                    allow_reasoning=allow_reasoning_cfg,
                )
            )

    return targets


def load_model_list(path: Path | None = None) -> list[str]:
    """Backward-compatible helper returning only model IDs."""
    return [target.model_id for target in load_model_targets(path)]


def add_model_to_yaml(model_id: str, path: Path | None = None) -> bool:
    """Append *model_id* to models.yaml if it is not already listed.

    Uses raw-text append to preserve comments and manual formatting.
    Returns True when the model was newly added, False when it was
    already present.
    """
    config_path = path or CONFIGS_PATH

    existing_ids = set(load_model_list(config_path))
    if model_id in existing_ids:
        return False

    if config_path.exists():
        content = config_path.read_text(encoding="utf-8")
    else:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        content = "models:\n"

    content = content.rstrip("\n") + f"\n\n  - {model_id}\n"
    config_path.write_text(content, encoding="utf-8")
    return True
