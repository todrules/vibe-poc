"""Route definitions for the requirement generation endpoint."""

import logging
import os
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import Settings, get_settings
from app.schemas.generate import GenerateRequest, GenerateResponse
from app.services.file_parser_service import FileParserService
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="", tags=["generate"])

# PROMPTS_DIR can override the default repository-relative prompts path in
# containerized environments.
_DEFAULT_PROMPTS_DIR = Path(__file__).resolve().parents[4] / "prompts"
_PROMPTS_DIR = Path(os.getenv("PROMPTS_DIR", str(_DEFAULT_PROMPTS_DIR)))


def _get_llm_service(settings: Settings = Depends(get_settings)) -> LLMService:
    """FastAPI dependency that constructs a fully configured ``LLMService``.

    Args:
        settings: Injected application settings.

    Returns:
        A ready-to-use ``LLMService`` instance.
    """
    return LLMService(settings=settings, prompts_dir=_PROMPTS_DIR)


@router.post(
    "/generate",
    response_model=GenerateResponse,
    response_model_by_alias=True,
    status_code=status.HTTP_200_OK,
    summary="Generate artifacts from requirement text",
    description=(
        "Accepts free-form requirement text (and optional uploaded file text), "
        "then returns structured acceptance criteria, agent prompts, user "
        "stories, and test cases produced by an OptnAI model."
    ),
)
def generate(
    request: GenerateRequest,
    llm_service: LLMService = Depends(_get_llm_service),
) -> GenerateResponse:
    """Process requirements and return generated artifacts.

    Args:
        request: Validated request payload containing requirement text and an
            optional uploaded file body.
        llm_service: Injected LLM service instance.

    Returns:
        A ``GenerateResponse`` containing all generated artifact categories.

    Raises:
        HTTPException 422: Re-raised from ``FileParserService`` when the
            merged requirement string is empty.
        HTTPException 502: Raised when the OptnAI API call fails.
        HTTPException 500: Raised when the LLM response cannot be parsed.
    """
    logger.info("POST /generate — merging inputs.")

    try:
        merged = FileParserService.merge(
            requirements=request.requirements,
            file_text=request.file_text,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    try:
        result = llm_service.generate(merged)
    except RuntimeError as exc:
        # OptnAI connectivity / authentication failure.
        logger.exception("OptnAI call failed.")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        # LLM returned unparseable or schema-mismatched JSON.
        logger.exception("Failed to parse LLM response.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    logger.info("POST /generate — completed successfully.")
    return result
