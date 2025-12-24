from __future__ import annotations

import time

try:
    import itchat  # type: ignore
except Exception as e:  # noqa: BLE001
    itchat = None  # type: ignore
    _IMPORT_ERROR = e
else:
    _IMPORT_ERROR = None

from wechat_assistant.llm import llm_reply
from wechat_assistant.settings import Settings


def main() -> int:
    settings = Settings.from_env()
    if itchat is None:
        print("未安装或无法导入 itchat，因此无法启用微信桥接。")
        print("你可以先正常使用 UI：python app.py")
        print("如需微信桥接：pip install -r requirements-wechat.txt")
        print(f"导入错误：{type(_IMPORT_ERROR).__name__}: {_IMPORT_ERROR}")
        return 2
    if not settings.wechat_auto_reply:
        print("WECHAT_AUTO_REPLY=false，已禁用微信自动回复。你仍可运行 UI：python app.py")
        return 0

    print("准备登录微信（itchat）。如果卡住/失败，不影响 UI 功能。")
    print("提示：首次登录可能会在终端显示二维码（enableCmdQR）。")

    # enableCmdQR 在无 GUI 环境更友好；热重载可减少重复扫码
    try:
        itchat.auto_login(hotReload=True, enableCmdQR=2)
    except TypeError:
        # 兼容老版本 itchat 参数差异
        itchat.auto_login(hotReload=True)

    @itchat.msg_register(itchat.content.TEXT)
    def on_text(msg):  # noqa: ANN001
        text = (msg.get("Text") or "").strip()
        if not text:
            return

        if settings.reply_delay_s > 0:
            time.sleep(settings.reply_delay_s)

        result = llm_reply(
            settings=settings,
            messages=[{"role": "user", "content": text}],
            system_prompt="你是一个简洁、友好的中文微信助手。回答尽量短。",
        )
        # 直接回复给来信方
        try:
            return result.text
        except Exception:
            return "（回复失败）"

    print("已登录，开始监听消息。按 Ctrl+C 退出。")
    itchat.run(blockThread=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

