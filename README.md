# WeChat AI Bot（itchat + 可选 Ollama）

这是一个**最小可运行**的微信个人号自动回复机器人：

- 使用 `itchat` 登录微信（控制台扫码）
- 收到文本消息后自动回复
- 可选接入本地 LLM（默认按 `.env.example` 使用 [Ollama] 的 `LLM_HOST`）

> 说明：当前实现是“个人号 + itchat”路线，不是公众号/企业微信的官方回调接口模式。

## 功能

- **自动回复开关**：`WECHAT_AUTO_REPLY`
- **回复延迟**：`REPLY_DELAY`
- **AI 回复开关**：`ENABLE_AI_REPLY`
- **本地 LLM（Ollama）**：`LLM_HOST` + `LLM_MODEL`
- **回复长度限制**：`MAX_RESPONSE_LENGTH`
- **彩色日志**：`LOG_LEVEL`

## 快速开始

### 1) 安装依赖

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) 配置环境变量

```bash
cp .env.example .env
```

按需修改 `.env`（关键项如下）：

```env
WECHAT_AUTO_REPLY=true
REPLY_DELAY=2
ENABLE_AI_REPLY=true
LLM_MODEL=mistral
LLM_HOST=http://localhost:11434
LOG_LEVEL=INFO
MAX_RESPONSE_LENGTH=200
```

### 3)（可选）启动 Ollama

如果你开启了 `ENABLE_AI_REPLY=true`，需要先让 Ollama 在本机运行并拉取模型，例如：

```bash
ollama serve
ollama pull mistral
```

### 4) 运行机器人

```bash
python app.py
```

首次运行会在控制台显示二维码，扫码登录后即可开始自动回复。

## 目录结构

- `app.py`：入口，itchat 消息处理与回复
- `utils/config.py`：从环境变量读取配置
- `utils/llm.py`：Ollama 客户端（`/api/generate`）
- `utils/logging_config.py`：彩色日志配置
