"""AI-related API routes."""

from fastapi import APIRouter

from app.api.deps import SessionDep

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/summarize")
async def summarize(
    session: SessionDep,
    text: str,
    max_length: int = 200,
) -> dict:
    """Summarize the given text using AI."""
    from app.services.ai_service import summarize_text

    summary = await summarize_text(text=text, max_length=max_length)
    return {
        "original_length": len(text),
        "summary": summary,
        "summary_length": len(summary),
    }
