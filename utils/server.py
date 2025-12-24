from __future__ import annotations

import asyncio
import threading
from typing import Any

from aiohttp import web
import psutil


def _build_health_payload() -> dict[str, Any]:
    vm = psutil.virtual_memory()
    return {
        "status": "ok",
        "cpu_percent": psutil.cpu_percent(interval=0.0),
        "memory": {
            "total": int(vm.total),
            "available": int(vm.available),
            "percent": float(vm.percent),
        },
    }


async def _run_app(host: str, port: int) -> None:
    app = web.Application()

    async def health(_request: web.Request) -> web.Response:
        return web.json_response(_build_health_payload())

    app.router.add_get("/health", health)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=host, port=port)
    await site.start()

    # Keep running forever in this thread
    while True:
        await asyncio.sleep(3600)


def start_health_server(*, host: str, port: int) -> None:
    """
    Start an aiohttp health server in a background thread.

    - GET /health -> JSON status + basic psutil metrics
    """

    def _target() -> None:
        asyncio.run(_run_app(host, port))

    t = threading.Thread(target=_target, name="health-server", daemon=True)
    t.start()
