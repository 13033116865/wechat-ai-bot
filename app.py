import time

import itchat
from dotenv import load_dotenv

from utils.config import load_config
from utils.llm import generate_ai_reply
from utils.logging_config import configure_logging


def main() -> None:
    load_dotenv()
    cfg = load_config()
    configure_logging(cfg.log_level)

    @itchat.msg_register(itchat.content.TEXT)
    def on_text_message(msg):  # type: ignore[no-untyped-def]
        # itchat message dict: https://itchat.readthedocs.io/zh/latest/intro/messages.html
        if not cfg.wechat_auto_reply:
            return None

        incoming = (msg.get("Text") or "").strip()
        if not incoming:
            return None

        if cfg.reply_delay > 0:
            time.sleep(cfg.reply_delay)

        if not cfg.enable_ai_reply:
            return incoming[: cfg.max_response_length]

        reply = generate_ai_reply(
            prompt=incoming,
            model=cfg.llm_model,
            host=cfg.llm_host,
            max_len=cfg.max_response_length,
        )
        return reply

    # NOTE: itchat login blocks; scan QR code in console.
    itchat.auto_login(hotReload=True)
    itchat.run()


if __name__ == "__main__":
    main()
