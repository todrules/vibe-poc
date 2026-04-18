"""Service abstraction for template loading and Azure OpenAI calls."""

from pathlib import Path


class LLMService:
    """Scaffold service for future LLM integration."""

    def __init__(self, prompts_dir: Path) -> None:
        self.prompts_dir = prompts_dir

    def load_template(self, template_name: str) -> str:
        template_path = self.prompts_dir / f"{template_name}.txt"
        return template_path.read_text(encoding="utf-8")
