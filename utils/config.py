from __future__ import annotations

import os
from dataclasses import dataclass


def _get_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


def _get_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(raw.strip())
    except ValueError:
        return default


def _get_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return float(raw.strip())
    except ValueError:
        return default


def _get_str(name: str, default: str) -> str:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip()


@dataclass(frozen=True)
class Config:
    wechat_auto_reply: bool
    reply_delay: float
    enable_ai_reply: bool
    llm_model: str
    llm_host: str
    log_level: str
    max_response_length: int
    rate_limit_per_minute: int
    history_max_items: int
    history_ttl_seconds: int
    enable_health_server: bool
    health_host: str
    health_port: int


def load_config() -> Config:
    return Config(
        wechat_auto_reply=_get_bool("WECHAT_AUTO_REPLY", True),
        reply_delay=_get_float("REPLY_DELAY", 0.0),
        enable_ai_reply=_get_bool("ENABLE_AI_REPLY", True),
        llm_model=_get_str("LLM_MODEL", "mistral"),
        llm_host=_get_str("LLM_HOST", "http://localhost:11434"),
        log_level=_get_str("LOG_LEVEL", "INFO"),
        max_response_length=_get_int("MAX_RESPONSE_LENGTH", 200),
        rate_limit_per_minute=_get_int("RATE_LIMIT_PER_MINUTE", 10),
        history_max_items=_get_int("HISTORY_MAX_ITEMS", 10),
        history_ttl_seconds=_get_int("HISTORY_TTL_SECONDS", 1800),
        enable_health_server=_get_bool("ENABLE_HEALTH_SERVER", False),
        health_host=_get_str("HEALTH_HOST", "127.0.0.1"),
        health_port=_get_int("HEALTH_PORT", 8000),
    )
