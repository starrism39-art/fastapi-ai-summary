"""AI service - calls OpenAI-compatible API with mock fallback."""

import httpx
from app.core.config import settings


class AIServiceError(Exception):
    """Raised when the AI service call fails."""


async def summarize_text(text: str, max_length: int = 200, language: str = "zh") -> str:
    """Summarize text using LLM, or mock if no API key configured."""
    if not settings.OPENAI_API_KEY:
        return _mock_summarize(text, max_length, language)

    return await _real_summarize(text, max_length, language)


async def _real_summarize(text: str, max_length: int, language: str) -> str:
    """Call OpenAI-compatible API."""
    prompt_lines = [
        f"请用{language}简洁总结以下内容（不超过{max_length}字）：",
        "",
        text,
    ]
    system_msg = "你是一个专业的文本摘要助手。请用简洁、准确的语言总结用户提供的内容。"

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{settings.OPENAI_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": settings.OPENAI_MODEL,
                    "messages": [
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": chr(10).join(prompt_lines)},
                    ],
                    "max_tokens": max_length * 2,
                    "temperature": 0.3,
                },
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except httpx.HTTPStatusError as e:
            raise AIServiceError(f"AI API returned {e.response.status_code}") from e
        except httpx.RequestError as e:
            raise AIServiceError(f"Failed to reach AI API: {e}") from e


def _mock_summarize(text: str, max_length: int, language: str) -> str:
    """Rule-based mock summary. No external dependencies needed."""
    cleaned = text.strip()
    if not cleaned:
        return "（无内容可总结）"

    prefix = cleaned[:max_length]
    sentences = cleaned.split("。")
    topic_sentences = [s.strip() for s in sentences if 10 < len(s) < 200]

    if topic_sentences:
        key_point = topic_sentences[0][:max_length]
    else:
        key_point = cleaned[:max_length]

    return (
        f"【Mock 摘要 - 未配置 API Key，使用规则生成】"
        f"该文本主要讨论了：{key_point}。"
        f"全文共 {len(cleaned)} 字，核心内容聚焦于上述主题。"
        f"（配置 OPENAI_API_KEY 或 Ollama 后可获得 AI 真实摘要）"
    )
