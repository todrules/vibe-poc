"""Application configuration placeholders."""

import os

from pydantic import BaseModel, Field


class Settings(BaseModel):
    azure_openai_endpoint: str = Field(...)
    azure_openai_api_key: str = Field(...)
    azure_openai_deployment: str = Field(...)

    @classmethod
    def from_env(cls) -> "Settings":
        """Load Azure OpenAI settings from environment variables."""
        return cls(
            azure_openai_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            azure_openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
            azure_openai_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        )
