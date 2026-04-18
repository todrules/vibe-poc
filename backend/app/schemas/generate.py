"""Pydantic schemas for /generate endpoint contracts."""

from typing import List

from pydantic import BaseModel, Field


class AgentPrompts(BaseModel):
    system: str = Field(default="")
    task: str = Field(default="")
    persona: str = Field(default="")


class GenerateRequest(BaseModel):
    """Request accepts normalized requirement text."""

    requirement_text: str = Field(min_length=1)


class GenerateResponse(BaseModel):
    """Strict response contract returned by LLM pipeline."""

    acceptance_criteria: List[str]
    agent_prompts: AgentPrompts
    user_stories: List[str]
    test_cases: List[str]
