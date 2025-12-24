import time

import itchat
import psutil
from dotenv import load_dotenv

from utils.config import load_config
from utils.history import InMemoryHistory
from utils.llm import generate_ai_reply
from utils.logging_config import configure_logging
from utils.rate_limit import SlidingWindowRateLimiter
from utils.server import start_health_server


def main() -> None:
    load_dotenv()
    cfg = load_config()
    configure_logging(cfg.log_level)

    limiter = SlidingWindowRateLimiter(limit=cfg.rate_limit_per_minute, window_s=60.0)
    history = InMemoryHistory(
        max_items_per_user=cfg.history_max_items, ttl_s=float(cfg.history_ttl_seconds)
    )

    if cfg.enable_health_server:
        start_health_server(host=cfg.health_host, port=cfg.health_port)

    @itchat.msg_register(itchat.content.TEXT)
    def on_text_message(msg):  # type: ignore[no-untyped-def]
        # itchat message dict: https://itchat.readthedocs.io/zh/latest/intro/messages.html
        if not cfg.wechat_auto_reply:
            return None

        incoming = (msg.get("Text") or "").strip()
        if not incoming:
            return None

        from_user = (msg.get("FromUserName") or "").strip() or "unknown"

        # Simple commands
        if incoming == "/help":
            return (
                "可用命令：\n"
                "/help 查看帮助\n"
                "/status 查看状态\n"
                "/clear_history 清空上下文\n"
            )
        if incoming == "/clear_history":
            history.clear(user_id=from_user)
            return "已清空上下文。"
        if incoming == "/status":
            vm = psutil.virtual_memory()
            return (
                "状态：运行中\n"
                f"AI：{'开' if cfg.enable_ai_reply else '关'}\n"
                f"模型：{cfg.llm_model}\n"
                f"LLM_HOST：{cfg.llm_host}\n"
                f"限流：{cfg.rate_limit_per_minute}/分钟\n"
                f"内存：{vm.percent:.1f}%\n"
            )

        if not limiter.allow(key=from_user):
            return "你发得有点快，稍后再试。"

        if cfg.reply_delay > 0:
            time.sleep(cfg.reply_delay)

        if not cfg.enable_ai_reply:
            return incoming[: cfg.max_response_length]

        # Append and build a compact context
        history.append(user_id=from_user, role="user", content=incoming)
        context = history.format_for_prompt(user_id=from_user, max_chars=1200)

        reply = generate_ai_reply(
            prompt=incoming,
            context=context,
            model=cfg.llm_model,
            host=cfg.llm_host,
            max_len=cfg.max_response_length,
        )
        history.append(user_id=from_user, role="assistant", content=reply)
        return reply

    # NOTE: itchat login blocks; scan QR code in console.
    itchat.auto_login(hotReload=True)
    itchat.run()


if __name__ == "__main__":
    main()
