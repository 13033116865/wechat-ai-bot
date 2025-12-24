from __future__ import annotations

import time


class SlidingWindowRateLimiter:
    """
    Simple in-memory per-key rate limiter.
    """

    def __init__(self, *, limit: int, window_s: float) -> None:
        self._limit = max(0, int(limit))
        self._window_s = float(window_s)
        self._hits: dict[str, list[float]] = {}

    def allow(self, *, key: str) -> bool:
        if self._limit <= 0:
            return True
        now = time.time()
        hits = self._hits.get(key, [])
        cutoff = now - self._window_s
        hits = [t for t in hits if t >= cutoff]
        if len(hits) >= self._limit:
            self._hits[key] = hits
            return False
        hits.append(now)
        self._hits[key] = hits
        return True
