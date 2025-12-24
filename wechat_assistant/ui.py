from __future__ import annotations

import os
from datetime import datetime

import gradio as gr

from wechat_assistant.llm import ollama_health, llm_reply
from wechat_assistant.settings import Settings


def _history_to_messages(history: list[tuple[str, str]]) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    for user, assistant in history:
        if user:
            messages.append({"role": "user", "content": user})
        if assistant:
            messages.append({"role": "assistant", "content": assistant})
    return messages


def build_ui(settings: Settings) -> gr.Blocks:
    with gr.Blocks(title="微信助手（本地部署）") as demo:
        gr.Markdown(
            "## 微信助手（本地部署）\n"
            "- **UI 聊天**：直接在本页对话\n"
            "- **LLM 默认对接 Ollama**：读取 `.env` 的 `LLM_HOST/LLM_MODEL`\n"
            "- **微信接入（可选）**：见“微信接入”页（依赖 itchat，能用则用）"
        )

        with gr.Tabs():
            with gr.Tab("聊天"):
                system_prompt = gr.Textbox(
                    label="系统提示词（可选）",
                    placeholder="例如：你是一个简洁的中文助手。",
                    lines=3,
                )

                debug = gr.Checkbox(label="显示调试信息（是否走了 fallback / 错误原因）", value=False)
                status = gr.Markdown(value="")

                def _respond(message: str, history: list[tuple[str, str]], sys: str, show_debug: bool):
                    messages = _history_to_messages(history)
                    messages.append({"role": "user", "content": message})

                    result = llm_reply(settings=settings, messages=messages, system_prompt=sys)
                    if show_debug:
                        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        detail = result.detail or ("fallback" if result.used_fallback else "ok")
                        status_md = f"**{ts}**｜used_fallback={result.used_fallback}｜{detail}"
                    else:
                        status_md = ""
                    return result.text, status_md

                chat = gr.ChatInterface(
                    fn=_respond,
                    additional_inputs=[system_prompt, debug],
                    additional_outputs=[status],
                    title="聊天",
                    description="如果你本机启动了 Ollama（默认 `http://localhost:11434`），会自动用它生成回复；否则会降级为本地回声回复。",
                )

                with gr.Accordion("连接状态 / 自检", open=False):
                    health_out = gr.Markdown(value="")

                    def _check():
                        ok, msg = ollama_health(settings)
                        if ok:
                            return f"**Ollama：可连接**（{settings.llm_host}）\n\n{msg}"
                        return f"**Ollama：不可用**（{settings.llm_host}）\n\n原因：{msg}"

                    gr.Button("检查 Ollama 连接").click(_check, outputs=[health_out])

            with gr.Tab("微信接入（可选）"):
                gr.Markdown(
                    "## 微信接入（可选）\n"
                    "本项目提供一个 **实验性** 的 itchat 桥接脚本：在终端登录微信后，收到文本消息会调用同一套 LLM 逻辑自动回复。\n\n"
                    "### 使用方法（建议先把项目放到桌面后再执行）\n"
                    "1. 复制 `.env.example` 为 `.env` 并按需修改（尤其是 `LLM_HOST/LLM_MODEL`）\n"
                    "2. 安装依赖：`pip install -r requirements.txt`\n"
                    "3. 运行桥接：`python -m wechat_assistant.wechat_itchat`\n\n"
                    "### 注意\n"
                    "- itchat 基于网页版/协议兼容性不稳定：**如果登录失败，不影响 UI 聊天功能**\n"
                    "- 自动回复是否开启受 `.env` 的 `WECHAT_AUTO_REPLY` 控制"
                )

            with gr.Tab("设置 / 配置说明"):
                gr.Markdown("## 当前配置（来自 `.env` + 默认值）")
                gr.JSON(
                    value={
                        "ENABLE_AI_REPLY": settings.enable_ai_reply,
                        "LLM_HOST": settings.llm_host,
                        "LLM_MODEL": settings.llm_model,
                        "LLM_TIMEOUT_S": settings.llm_timeout_s,
                        "MAX_RESPONSE_LENGTH": settings.max_response_length,
                        "WECHAT_AUTO_REPLY": settings.wechat_auto_reply,
                        "REPLY_DELAY": settings.reply_delay_s,
                    }
                )

        gr.Markdown(
            "---\n"
            "如果你希望“文件在桌面直接双击/一键启动”，请看仓库里的 `scripts/install_to_desktop.sh`（Linux）或 `scripts/install_to_desktop.bat`（Windows，若提供）。"
        )

    return demo


def main() -> None:
    settings = Settings.from_env()
    demo = build_ui(settings)

    # 默认只在本机开放；需要局域网访问可设置 GRADIO_SERVER_NAME=0.0.0.0
    server_name = os.getenv("GRADIO_SERVER_NAME", "127.0.0.1")
    server_port = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
    demo.launch(server_name=server_name, server_port=server_port)

