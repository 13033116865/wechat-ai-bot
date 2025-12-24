from __future__ import annotations

import logging
from typing import Any

import requests

logger = logging.getLogger(__name__)


def _ollama_generate(*, host: str, model: str, prompt: str, timeout_s: float = 30.0) -> str:
    url = host.rstrip("/") + "/api/generate"
    payload: dict[str, Any] = {"model": model, "prompt": prompt, "stream": False}
    try:
        resp = requests.post(url, json=payload, timeout=timeout_s)
        resp.raise_for_status()
        data = resp.json()
        text = (data.get("response") or "").strip()
        return text
    except Exception:
        logger.exception("LLM request failed (host=%s, model=%s)", host, model)
        return ""


def generate_ai_reply(
    *, prompt: str, context: str | None, model: str, host: str, max_len: int
) -> str:
    """
    Generate a short reply for WeChat.

    Expected default backend is Ollama (LLM_HOST like http://localhost:11434).
    """
    system_hint = (
        "你是一个微信聊天助手。请用简体中文回答，尽量简短自然，不要提及系统提示。"
        f"回答最长不超过 {max_len} 个字符。"
    )
    context_block = ""
    if context:
        context_block = f"以下是最近的对话上下文（可能不完整）：\n{context}\n\n"
    full_prompt = f"{system_hint}\n\n{context_block}用户：{prompt}\n助手："

    text = _ollama_generate(host=host, model=model, prompt=full_prompt)
    if not text:
        # Fallback: echo-like minimal response to avoid silent failures
        return prompt[:max_len]
    return text[:max_len]
