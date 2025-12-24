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
- **每用户限流**：`RATE_LIMIT_PER_MINUTE`
- **短期上下文**：`HISTORY_MAX_ITEMS` / `HISTORY_TTL_SECONDS`
- **健康检查**：`ENABLE_HEALTH_SERVER`（`GET /health`）

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

## 命令

- `/help`：查看帮助
- `/status`：查看当前状态（含模型/限流/内存占用）
- `/clear_history`：清空当前会话的短期上下文
- `/stats`：近 7 天消息统计（需开启 SQLite 日志）

## 白名单（可选）

如果你只希望机器人回复特定联系人，可以在 `.env` 里配置：

```env
ALLOW_USERNAMES=wxid_xxx,wxid_yyy
```

这里的值对应 itchat 消息里的 `FromUserName`（通常是 `wxid_...`）。留空表示允许所有人。

## 群聊（可选）

默认**不**在群聊里回复。开启后，只有当消息以指定前缀开头才会触发回复（避免刷屏）：

```env
ENABLE_GROUP_CHAT=true
GROUP_CHAT_TRIGGER_PREFIX=/bot 
```

例如群里发送：`/bot 你好` 才会触发回复。

## SQLite 日志与统计

默认会把“收到的消息/回复”写入 SQLite（用于 `/stats`）：

```env
ENABLE_SQLITE_LOG=true
DB_PATH=data/bot.sqlite3
```

## 健康检查（可选）

启用后会在后台线程启动一个 HTTP 服务：

- `GET /health`：返回 JSON（含 CPU/内存等基本指标）

相关环境变量：

- `ENABLE_HEALTH_SERVER=true`
- `HEALTH_HOST=127.0.0.1`
- `HEALTH_PORT=8000`

## 目录结构

- `app.py`：入口，itchat 消息处理与回复
- `utils/config.py`：从环境变量读取配置
- `utils/llm.py`：Ollama 客户端（`/api/generate`）
- `utils/logging_config.py`：彩色日志配置
- `utils/history.py`：内存版短期上下文
- `utils/rate_limit.py`：简单限流
- `utils/server.py`：aiohttp `/health`
