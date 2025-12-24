from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


def _to_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _to_int(value: str | None, default: int) -> int:
    if value is None:
        return default
    try:
        return int(value.strip())
    except ValueError:
        return default


def _to_float(value: str | None, default: float) -> float:
    if value is None:
        return default
    try:
        return float(value.strip())
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    # General
    log_level: str
    max_response_length: int

    # LLM (default: Ollama)
    enable_ai_reply: bool
    llm_model: str
    llm_host: str
    llm_timeout_s: float

    # WeChat (optional)
    wechat_auto_reply: bool
    reply_delay_s: float

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()

        return cls(
            log_level=os.getenv("LOG_LEVEL", "INFO").strip(),
            max_response_length=_to_int(os.getenv("MAX_RESPONSE_LENGTH"), 200),
            enable_ai_reply=_to_bool(os.getenv("ENABLE_AI_REPLY"), True),
            llm_model=os.getenv("LLM_MODEL", "mistral").strip(),
            llm_host=os.getenv("LLM_HOST", "http://localhost:11434").strip().rstrip("/"),
            llm_timeout_s=_to_float(os.getenv("LLM_TIMEOUT_S"), 60.0),
            wechat_auto_reply=_to_bool(os.getenv("WECHAT_AUTO_REPLY"), True),
            reply_delay_s=_to_float(os.getenv("REPLY_DELAY"), 2.0),
        )

