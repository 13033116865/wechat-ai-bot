# WeChat AI Bot

A powerful AI-powered WeChat bot that brings intelligent conversation capabilities to your WeChat ecosystem. This bot leverages advanced language models to provide natural, context-aware responses to user messages.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Quick Start Guide](#quick-start-guide)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Integration](#api-integration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

WeChat AI Bot is a modern chatbot solution designed specifically for WeChat platform integration. It combines WeChat's messaging infrastructure with state-of-the-art AI language models to create an intelligent, responsive assistant capable of handling diverse conversation scenarios including customer service, information queries, and general conversation.

### Key Benefits

- **Seamless Integration**: Direct integration with WeChat's official API
- **AI-Powered Responses**: Leverages advanced language models for intelligent replies
- **High Performance**: Optimized for low-latency responses
- **Scalable Architecture**: Designed to handle multiple concurrent conversations
- **Easy Deployment**: Simple setup and configuration process

## Features

### 🤖 AI Capabilities

- **Natural Language Processing**: Understands context and intent from user messages
- **Multi-language Support**: Handles conversations in multiple languages
- **Contextual Awareness**: Maintains conversation history for better response quality
- **Intent Recognition**: Automatically identifies user intent and routes appropriately

### 💬 Messaging Features

- **Text Messages**: Full support for text-based conversations
- **Media Handling**: Process and respond to images, files, and multimedia content
- **Message Routing**: Intelligent routing of messages to appropriate handlers
- **Typing Indicators**: Shows when bot is processing responses
- **Message Formatting**: Rich text formatting and structured responses

### ⚙️ System Features

- **Auto-reply**: Automatic responses to messages during specified hours
- **Rate Limiting**: Built-in protection against message flooding
- **Error Handling**: Graceful error handling with user-friendly messages
- **Logging**: Comprehensive logging for monitoring and debugging
- **Admin Controls**: Administrative interface for bot management

### 📊 Advanced Capabilities

- **Analytics**: Track bot performance and user engagement metrics
- **Custom Workflows**: Define custom response patterns and behaviors
- **Integration Ready**: Easy integration with external services and APIs
- **Configuration Management**: Flexible configuration system

## System Requirements

### Software Requirements

- **Python**: 3.8 or higher
- **Operating System**: Linux, macOS, or Windows
- **Node.js**: 14.0 or higher (for certain components)

### Runtime Requirements

- **Memory**: Minimum 2GB RAM, recommended 4GB+
- **Storage**: 500MB free disk space
- **Network**: Stable internet connection with low latency
- **Bandwidth**: 1 Mbps or higher recommended

### Dependencies

- WeChat Official API credentials
- An AI language model API key (OpenAI, Hugging Face, or similar)
- Database (PostgreSQL recommended, SQLite supported)
- Redis (optional, for caching and sessions)

### Development Requirements (Optional)

- Docker (for containerized deployment)
- Git (for version control)
- pip/poetry (Python package managers)

## Installation

### 1. Prerequisites Setup

Ensure you have Python 3.8+ installed:

```bash
python --version
```

### 2. Clone the Repository

```bash
git clone https://github.com/13033116865/wechat-ai-bot.git
cd wechat-ai-bot
```

### 3. Create Virtual Environment

```bash
# On macOS/Linux
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
nano .env  # or use your preferred editor
```

### 6. Initialize Database

```bash
python manage.py migrate
```

### 7. Create Admin User

```bash
python manage.py createsuperuser
```

## Quick Start Guide

### Step 1: Set Up WeChat Credentials

1. Register for a WeChat Official Account at [mp.weixin.qq.com](https://mp.weixin.qq.com)
2. Get your AppID and AppSecret from the admin console
3. Add the following to your `.env` file:

```env
WECHAT_APP_ID=your_app_id_here
WECHAT_APP_SECRET=your_app_secret_here
WECHAT_TOKEN=your_token_here
WECHAT_ENCODING_AES_KEY=your_aes_key_here
```

### Step 2: Configure AI Model

Add your AI provider credentials to `.env`:

```env
# For OpenAI
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-3.5-turbo

# Or for other providers
AI_PROVIDER=openai  # options: openai, huggingface, anthropic
```

### Step 3: Set Server Configuration

```env
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=False
LOG_LEVEL=INFO
```

### Step 4: Start the Bot

```bash
# Development mode
python app.py

# Production mode with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Step 5: Set WeChat Webhook

1. Go to WeChat Official Account admin panel
2. Navigate to Basic Settings → Server Configuration
3. Set the callback URL to: `https://your-domain.com/wechat/callback`
4. Set the token (must match WECHAT_TOKEN in .env)
5. Click "Submit" to verify

### Step 6: Test the Bot

Send a message to your WeChat Official Account and verify the bot responds appropriately.

## Configuration

### Environment Variables Reference

```env
# WeChat Configuration
WECHAT_APP_ID=                          # Your WeChat App ID
WECHAT_APP_SECRET=                      # Your WeChat App Secret
WECHAT_TOKEN=                           # Webhook token
WECHAT_ENCODING_AES_KEY=                # Message encryption key

# AI Provider Configuration
AI_PROVIDER=openai                      # AI provider (openai, huggingface, etc.)
OPENAI_API_KEY=                         # OpenAI API key
OPENAI_MODEL=gpt-3.5-turbo             # Model to use

# Server Configuration
SERVER_HOST=0.0.0.0                    # Server host
SERVER_PORT=8000                       # Server port
SERVER_URL=https://your-domain.com     # Public server URL
DEBUG=False                            # Debug mode
LOG_LEVEL=INFO                         # Logging level

# Database Configuration
DATABASE_URL=postgresql://user:pass@localhost/dbname
DATABASE_POOL_SIZE=5

# Cache Configuration (Optional)
REDIS_URL=redis://localhost:6379      # Redis connection

# Bot Behavior
BOT_TIMEOUT=30                         # Response timeout in seconds
MAX_MESSAGE_LENGTH=2000                # Max message length
RATE_LIMIT_ENABLED=True               # Enable rate limiting
RATE_LIMIT_PER_MINUTE=10              # Messages per minute per user
```

### Configuration Files

- `config.yaml`: Main configuration file
- `.env`: Environment variables (create from `.env.example`)
- `logging.config`: Logging configuration

## Usage

### Basic Message Handling

The bot automatically processes incoming WeChat messages and generates responses using the configured AI model.

### Admin Dashboard

Access the admin dashboard at `https://your-domain.com/admin` to:

- Monitor bot conversations
- View analytics and statistics
- Manage user preferences
- Configure response settings
- View logs and errors

### Command Syntax

Use special commands to control bot behavior:

```
/help              - Show available commands
/status            - Check bot status
/config            - View current configuration
/clear_history     - Clear conversation history
/reset             - Reset bot state
```

## API Integration

### Webhook Endpoint

**POST** `/wechat/callback`

Receives and processes incoming WeChat messages.

### Message Format

```json
{
  "FromUserName": "user_id",
  "ToUserName": "bot_id",
  "CreateTime": 1234567890,
  "MsgType": "text",
  "Content": "User message",
  "MsgId": "1234567890"
}
```

### Response Format

```json
{
  "ToUserName": "user_id",
  "FromUserName": "bot_id",
  "CreateTime": 1234567890,
  "MsgType": "text",
  "Content": "Bot response",
  "MsgId": "1234567890"
}
```

## Troubleshooting

### Common Issues

#### Bot not responding

1. Check if the server is running: `curl http://localhost:8000/health`
2. Verify WeChat credentials in `.env`
3. Check logs: `tail -f logs/app.log`
4. Ensure webhook URL is correctly configured

#### Message timeout

1. Check AI provider connection
2. Increase `BOT_TIMEOUT` in `.env`
3. Monitor server resources (CPU, memory)
4. Check network connectivity

#### Database connection errors

1. Verify DATABASE_URL is correct
2. Ensure database service is running
3. Check database permissions
4. Review logs for specific error messages

### Debug Mode

Enable debug logging for troubleshooting:

```env
DEBUG=True
LOG_LEVEL=DEBUG
```

### Support

For issues and questions:
- Check existing GitHub issues
- Create a new issue with detailed information
- Include logs and configuration (without sensitive data)

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a pull request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linter
flake8 .

# Format code
black .
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Last Updated**: 2025-12-24

For the latest updates and documentation, visit [GitHub Repository](https://github.com/13033116865/wechat-ai-bot)
