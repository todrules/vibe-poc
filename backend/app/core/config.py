"""Application configuration placeholders."""

from pydantic import BaseModel, Field


class Settings(BaseModel):
    azure_openai_endpoint: str = Field(...)
    azure_openai_api_key: str = Field(...)
    azure_openai_deployment: str = Field(...)
