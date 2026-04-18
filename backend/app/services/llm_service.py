"""Service abstraction for template loading and Azure OpenAI calls."""

import re
from pathlib import Path


class LLMService:
    """Scaffold service for future LLM integration."""

    def __init__(self, prompts_dir: Path) -> None:
        self.prompts_dir = prompts_dir

    def load_template(self, template_name: str) -> str:
        if not re.fullmatch(r"[a-zA-Z0-9_-]+", template_name):
            msg = "Invalid template name format."
            raise ValueError(msg)

        prompts_dir = self.prompts_dir.resolve()
        template_path = (prompts_dir / f"{template_name}.txt").resolve()
        if not template_path.is_relative_to(prompts_dir):
            msg = "Template path is outside prompts directory."
            raise ValueError(msg)

        return template_path.read_text(encoding="utf-8")
