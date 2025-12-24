# 微信助手（本地部署，带 UI）

这个项目提供一个**本地网页 UI**（聊天窗口），默认对接你电脑上的 **Ollama**（可选）。你可以把整个文件夹放到桌面，在浏览器里使用。

## 你会得到什么

- **UI 界面**：运行后打开浏览器即可聊天（默认端口 `7860`）
- **本地 LLM（可选）**：默认走 `.env` 的 `LLM_HOST/LLM_MODEL`（适配 Ollama）
- **微信接入（可选）**：提供 `itchat` 桥接脚本；兼容性不稳定，失败不影响 UI 使用

## 快速部署到桌面（Linux）

在项目根目录执行：

```bash
chmod +x scripts/install_to_desktop.sh
./scripts/install_to_desktop.sh
```

脚本会把文件复制到桌面：`~/Desktop/WeChatAssistant`（或你的系统桌面目录），然后按提示进入目录并启动。

## 启动 UI（推荐）

进入桌面目录后：

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

启动后在浏览器打开：`http://127.0.0.1:7860`

### （可选）启用 Ollama

如果你已经安装 Ollama，并且本机能访问 `http://localhost:11434`，UI 会自动调用它生成回复。

常用配置（写到 `.env`）：

```env
LLM_HOST=http://localhost:11434
LLM_MODEL=mistral
```

## （可选）微信桥接（itchat）

仅当你确认 `itchat` 在你的环境可用时再尝试：

```bash
pip install -r requirements-wechat.txt
python -m wechat_assistant.wechat_itchat
```

如果登录失败/不兼容：这是预期情况之一，**不影响 UI 功能**。

## 配置说明

参考 `.env.example`。常用项：

- **ENABLE_AI_REPLY**：是否启用 LLM（默认 `true`）
- **MAX_RESPONSE_LENGTH**：回复最大字符数（默认 `200`）
- **GRADIO_SERVER_NAME/PORT**：UI 监听地址/端口（默认 `127.0.0.1:7860`）
