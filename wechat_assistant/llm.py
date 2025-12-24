from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests

from wechat_assistant.settings import Settings


@dataclass(frozen=True)
class LLMResult:
    text: str
    used_fallback: bool
    detail: str | None = None


def _truncate(text: str, max_len: int) -> str:
    if max_len <= 0:
        return text
    return text if len(text) <= max_len else text[: max_len - 1] + "…"


def _fallback_reply(messages: list[dict[str, str]], settings: Settings) -> LLMResult:
    last_user = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            last_user = (m.get("content") or "").strip()
            break
    if not last_user:
        return LLMResult(text="你好！我在。", used_fallback=True)

    # 超轻量规则：能用就行，不做“伪智能”承诺
    if "帮助" in last_user or "help" in last_user.lower():
        text = (
            "我已经启动了本地 UI。你可以：\n"
            "- 直接在这里聊天\n"
            "- 如果你本机装了 Ollama，会自动用它生成回复\n"
            "- 想接入微信的话，按“微信接入”页的说明运行桥接脚本"
        )
        return LLMResult(text=_truncate(text, settings.max_response_length), used_fallback=True)

    return LLMResult(
        text=_truncate(f"（未连接到本地 LLM，先回声）你说：{last_user}", settings.max_response_length),
        used_fallback=True,
    )


def ollama_chat(
    *,
    settings: Settings,
    messages: list[dict[str, str]],
    system_prompt: str | None = None,
) -> LLMResult:
    """
    Call Ollama chat endpoint:
    POST {LLM_HOST}/api/chat
    """
    payload: dict[str, Any] = {
        "model": settings.llm_model,
        "stream": False,
        "messages": [],
    }

    if system_prompt and system_prompt.strip():
        payload["messages"].append({"role": "system", "content": system_prompt.strip()})

    # Expect already {role, content}; keep only required keys
    for m in messages:
        role = (m.get("role") or "").strip()
        content = (m.get("content") or "").strip()
        if role and content:
            payload["messages"].append({"role": role, "content": content})

    url = f"{settings.llm_host}/api/chat"
    resp = requests.post(url, json=payload, timeout=settings.llm_timeout_s)
    resp.raise_for_status()
    data = resp.json()

    content = (
        (data.get("message") or {}).get("content")
        if isinstance(data, dict)
        else None
    )
    if not content:
        return LLMResult(text="（Ollama 返回为空）", used_fallback=True, detail="empty_response")

    return LLMResult(text=_truncate(str(content), settings.max_response_length), used_fallback=False)


def llm_reply(
    *,
    settings: Settings,
    messages: list[dict[str, str]],
    system_prompt: str | None = None,
) -> LLMResult:
    if not settings.enable_ai_reply:
        return _fallback_reply(messages, settings)
    try:
        return ollama_chat(settings=settings, messages=messages, system_prompt=system_prompt)
    except Exception as e:  # noqa: BLE001 - keep UX stable
        r = _fallback_reply(messages, settings)
        return LLMResult(
            text=r.text,
            used_fallback=True,
            detail=f"ollama_error: {type(e).__name__}: {e}",
        )


def ollama_health(settings: Settings) -> tuple[bool, str]:
    """
    Best-effort health check.
    """
    try:
        resp = requests.get(f"{settings.llm_host}/api/tags", timeout=min(5.0, settings.llm_timeout_s))
        if resp.status_code != 200:
            return False, f"HTTP {resp.status_code}"
        data = resp.json()
        models = []
        if isinstance(data, dict) and isinstance(data.get("models"), list):
            for m in data["models"]:
                name = (m or {}).get("name")
                if name:
                    models.append(str(name))
        if models:
            return True, "可用模型示例：" + ", ".join(models[:8])
        return True, "Ollama 可连接，但未返回模型列表"
    except Exception as e:  # noqa: BLE001
        return False, f"{type(e).__name__}: {e}"

