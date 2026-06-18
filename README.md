# FastAPI Backend + AI Summary

基于 [FastAPI Full Stack Template](https://github.com/fastapi/full-stack-fastapi-template) 扩展的 AI 摘要接口。

## ✨ 新增功能

### AI 摘要接口 (POST /ai/summarize)

- 调用 OpenAI 兼容 API（OpenAI / Ollama）进行文本摘要
- 异步请求（httpx），支持超时与错误处理
- 未配置 API Key 时自动降级为 Mock 摘要（无需外部依赖）

`python
POST /ai/summarize
Body: text=\"需要摘要的文本\"&max_length=200
Response: { \"summary\": \"...\", \"original_length\": N, \"summary_length\": N }
`

### 测试覆盖

ackend/tests/api/routes/test_ai.py — 3 个 pytest 用例：
- 正常摘要请求
- 空文本处理
- API Key 缺失时的 Mock 回退

## 技术栈

| 模块 | 技术 |
|------|------|
| 后端框架 | FastAPI + Python 3.12 |
| 数据库 ORM | SQLModel + PostgreSQL |
| 认证 | JWT（密码哈希 + Token） |
| 部署 | Docker Compose + Traefik |

## 快速开始

### 1. 配置环境变量

`ash
cp .env.example .env
`

根据需要修改 .env 中的配置项：

- OPENAI_API_KEY：可选，留空则使用 Mock 摘要
- OPENAI_BASE_URL：默认 OpenAI，可改为本地 Ollama (http://localhost:11434/v1)
- OPENAI_MODEL：默认 gpt-4o-mini

### 2. 启动

`ash
docker compose up -d
`

访问 http://localhost:5173 进入前端页面，登录后可在侧边栏使用 AI 摘要功能。

## 测试

`ash
docker compose exec backend bash -c \"pytest -v\"
`

## 说明

本项目基于全栈模板搭建，在保留原有用户认证、CRUD 功能的基础上，**独立扩展了 AI 摘要服务**（/app/services/ai_service.py + /app/api/routes/ai.py），包含完整的单元测试覆盖。
