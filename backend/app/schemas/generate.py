"""Pydantic schemas for /generate endpoint contracts."""

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class _CamelModel(BaseModel):
    """Base model that serialises field names as camelCase JSON keys."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class AcceptanceCriteriaItem(_CamelModel):
    """A single acceptance criterion expressed as a title and Gherkin scenario."""

    title: str = Field(description="Short descriptive title for the criterion.")
    gherkin: str = Field(
        description="Full Gherkin scenario (Given/When/Then) for the criterion."
    )


class AgentPrompts(_CamelModel):
    """Prompt fragments returned for use in downstream AI agents."""

    system: str = Field(default="", description="System-level instructions.")
    task: str = Field(default="", description="Task description for the agent.")
    persona: str = Field(default="", description="Persona framing for the agent.")


class GenerateRequest(_CamelModel):
    """Request payload accepted by POST /generate."""

    requirements: str = Field(
        min_length=1,
        description="Free-form requirement text entered by the user.",
    )
    file_text: str | None = Field(
        default=None,
        description="Optional supplementary text extracted from an uploaded file.",
    )


class GenerateResponse(_CamelModel):
    """Structured artifacts returned after processing the requirements."""

    acceptance_criteria: list[AcceptanceCriteriaItem] = Field(
        description="Gherkin-formatted acceptance criteria."
    )
    agent_prompts: AgentPrompts = Field(
        description="System, task, and persona prompts for AI agents."
    )
    user_stories: list[str] = Field(description="User stories in standard format.")
    test_cases: list[str] = Field(description="High-level test case descriptions.")
