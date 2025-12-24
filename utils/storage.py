from __future__ import annotations

import os
import sqlite3
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class DailyStats:
    day: str  # YYYY-MM-DD
    messages: int


class SQLiteStore:
    def __init__(self, *, db_path: str) -> None:
        self._db_path = db_path
        self._ensure_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_db(self) -> None:
        parent = os.path.dirname(self._db_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS message_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts REAL NOT NULL,
                    user_id TEXT NOT NULL,
                    is_group INTEGER NOT NULL,
                    incoming TEXT NOT NULL,
                    reply TEXT NOT NULL
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_message_log_ts ON message_log(ts)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_message_log_user ON message_log(user_id)"
            )

    def log_message(
        self, *, user_id: str, is_group: bool, incoming: str, reply: str
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO message_log(ts, user_id, is_group, incoming, reply) VALUES (?, ?, ?, ?, ?)",
                (time.time(), user_id, 1 if is_group else 0, incoming, reply),
            )

    def get_daily_stats(self, *, days: int = 7) -> list[DailyStats]:
        days = max(1, int(days))
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT
                  date(ts, 'unixepoch', 'localtime') AS day,
                  count(*) AS messages
                FROM message_log
                WHERE ts >= (strftime('%s','now') - ?)
                GROUP BY day
                ORDER BY day DESC
                """,
                (days * 86400,),
            ).fetchall()
        return [DailyStats(day=str(r["day"]), messages=int(r["messages"])) for r in rows]
