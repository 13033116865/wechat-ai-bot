from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass
class HistoryItem:
    role: str  # "user" | "assistant"
    content: str
    ts: float


class InMemoryHistory:
    """
    Very small in-memory per-user history with TTL.
    """

    def __init__(self, *, max_items_per_user: int = 10, ttl_s: float = 1800.0) -> None:
        self._max_items = max_items_per_user
        self._ttl_s = ttl_s
        self._data: dict[str, list[HistoryItem]] = {}

    def _gc_user(self, user_id: str) -> None:
        now = time.time()
        items = self._data.get(user_id)
        if not items:
            return
        items = [it for it in items if now - it.ts <= self._ttl_s]
        if items:
            self._data[user_id] = items[-self._max_items :]
        else:
            self._data.pop(user_id, None)

    def append(self, *, user_id: str, role: str, content: str) -> None:
        self._gc_user(user_id)
        items = self._data.setdefault(user_id, [])
        items.append(HistoryItem(role=role, content=content, ts=time.time()))
        self._data[user_id] = items[-self._max_items :]

    def clear(self, *, user_id: str) -> None:
        self._data.pop(user_id, None)

    def format_for_prompt(self, *, user_id: str, max_chars: int = 1200) -> str:
        self._gc_user(user_id)
        items = self._data.get(user_id, [])
        lines: list[str] = []
        for it in items:
            prefix = "用户" if it.role == "user" else "助手"
            lines.append(f"{prefix}：{it.content}")
        text = "\n".join(lines).strip()
        if len(text) > max_chars:
            text = text[-max_chars:]
        return text
