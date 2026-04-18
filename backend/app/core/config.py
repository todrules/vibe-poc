"""Application configuration placeholders."""

from pydantic import BaseModel


class Settings(BaseModel):
    azure_openai_endpoint: str = ""
    azure_openai_api_key: str = ""
    azure_openai_deployment: str = ""
