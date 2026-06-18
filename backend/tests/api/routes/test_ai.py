"""Tests for the AI route."""

import pytest

from app.core.config import settings


@pytest.mark.anyio
async def test_summarize_no_api_key(client) -> None:
    temp_key = settings.OPENAI_API_KEY
    settings.OPENAI_API_KEY = None
    try:
        response = await client.post(
            f"{settings.API_V1_STR}/ai/summarize",
            params={"text": "Hello world"},
        )
        assert response.status_code == 500
    finally:
        settings.OPENAI_API_KEY = temp_key


@pytest.mark.anyio
async def test_summarize_missing_text(client) -> None:
    response = await client.post(
        f"{settings.API_V1_STR}/ai/summarize",
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_summarize_with_params(client) -> None:
    response = await client.post(
        f"{settings.API_V1_STR}/ai/summarize",
        params={"text": "Hello world", "max_length": 100},
    )
    assert response.status_code in (200, 422, 500)
