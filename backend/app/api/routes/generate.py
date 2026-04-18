"""Route definitions for requirement generation."""

from fastapi import APIRouter

from app.schemas.generate import GenerateRequest, GenerateResponse

router = APIRouter(prefix="", tags=["generate"])


@router.post("/generate", response_model=GenerateResponse)
def generate(_: GenerateRequest) -> GenerateResponse:
    """Stub endpoint; implementation will be added incrementally."""
    return GenerateResponse(
        acceptance_criteria=[],
        agent_prompts={"system": "", "task": "", "persona": ""},
        user_stories=[],
        test_cases=[],
    )
