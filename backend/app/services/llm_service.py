"""Service for loading prompt templates and calling the OptnAI API."""

import json
import logging
import re
from pathlib import Path

from openai import OpenAI, OpenAIError

from app.core.config import Settings
from app.schemas.generate import (
    AcceptanceCriteriaItem,
    AgentPrompts,
    GenerateResponse,
)

logger = logging.getLogger(__name__)

# Describes the expected JSON shape embedded inside the system prompt so the
# model understands the required output contract.
_RESPONSE_SCHEMA_HINT = """
Return ONLY valid JSON with this exact shape — no markdown fences, no extra keys:
{
  "acceptanceCriteria": [
    {"title": "<string>", "gherkin": "<Given/When/Then scenario>"}
  ],
  "agentPrompts": {
    "system": "<system instructions>",
    "task": "<task description>",
    "persona": "<persona framing>"
  },
  "userStories": ["<As a … I want … so that …>"],
  "testCases": ["<test case description>"]
}
""".strip()


class LLMService:
    """Orchestrates prompt construction and OptnAI chat completion calls.

    Args:
        settings: Application settings containing OptnAI credentials.
        prompts_dir: Filesystem path to the directory containing ``.txt``
            prompt templates (``system.txt``, ``task.txt``, ``persona.txt``).
    """

    def __init__(self, settings: Settings, prompts_dir: Path) -> None:
        self._prompts_dir = prompts_dir.resolve()
        self._client = OpenAI(
            api_key=settings.optnai_api_key,
            base_url=settings.optnai_base_url,
        )
        self._model = settings.optnai_model

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(self, merged_requirements: str) -> GenerateResponse:
        """Run the full generation pipeline for the supplied requirement text.

        Args:
            merged_requirements: Pre-processed requirement string produced by
                ``FileParserService.merge()``.

        Returns:
            A fully populated ``GenerateResponse`` instance.

        Raises:
            ValueError: If the LLM returns a response that cannot be parsed
                as valid JSON or does not match the expected schema.
            RuntimeError: If the OptnAI API call fails.
        """
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(merged_requirements)

        logger.debug("Calling OptnAI model '%s'.", self._model)
        raw_json = self._call_optnai(system_prompt, user_prompt)

        return self._parse_response(raw_json)

    # ------------------------------------------------------------------
    # Prompt construction
    # ------------------------------------------------------------------

    def _build_system_prompt(self) -> str:
        """Combine the system template with the JSON response schema hint.

        Returns:
            The fully assembled system prompt string.
        """
        system_template = self._load_template("system")
        return f"{system_template}\n\n{_RESPONSE_SCHEMA_HINT}"

    def _build_user_prompt(self, merged_requirements: str) -> str:
        """Combine the persona and task templates with the requirement text.

        Args:
            merged_requirements: Normalised requirement string.

        Returns:
            The fully assembled user prompt string.
        """
        persona_template = self._load_template("persona")
        task_template = self._load_template("task")
        return (
            f"{persona_template}\n\n"
            f"{task_template}\n\n"
            f"--- Requirements ---\n{merged_requirements}"
        )

    # ------------------------------------------------------------------
    # OptnAI interaction
    # ------------------------------------------------------------------

    def _call_optnai(self, system_prompt: str, user_prompt: str) -> str:
        """Send the assembled prompts to OptnAI and return the raw text.

        Args:
            system_prompt: System-role message content.
            user_prompt: User-role message content.

        Returns:
            Raw text content of the first completion choice.

        Raises:
            RuntimeError: Wraps any ``OpenAIError`` raised by the SDK so
                callers receive a consistent exception type.
        """
        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
            )
        except OpenAIError as exc:
            logger.exception("OptnAI API call failed.")
            raise RuntimeError(f"OptnAI request failed: {exc}") from exc

        content = response.choices[0].message.content or ""
        logger.debug("Raw LLM response: %s", content)
        return content

    # ------------------------------------------------------------------
    # Response parsing
    # ------------------------------------------------------------------

    def _parse_response(self, raw_json: str) -> GenerateResponse:
        """Deserialise and validate the LLM's JSON output.

        Args:
            raw_json: Raw JSON string returned by the model.

        Returns:
            A validated ``GenerateResponse`` instance.

        Raises:
            ValueError: If ``raw_json`` is not valid JSON or is missing
                required fields.
        """
        try:
            data: dict = json.loads(raw_json)
        except json.JSONDecodeError as exc:
            raise ValueError(f"LLM returned invalid JSON: {exc}") from exc

        try:
            acceptance_criteria = [
                AcceptanceCriteriaItem(
                    title=item["title"],
                    gherkin=item["gherkin"],
                )
                for item in data.get("acceptanceCriteria", [])
            ]

            raw_prompts: dict = data.get("agentPrompts", {})
            agent_prompts = AgentPrompts(
                system=raw_prompts.get("system", ""),
                task=raw_prompts.get("task", ""),
                persona=raw_prompts.get("persona", ""),
            )

            return GenerateResponse(
                acceptance_criteria=acceptance_criteria,
                agent_prompts=agent_prompts,
                user_stories=data.get("userStories", []),
                test_cases=data.get("testCases", []),
            )
        except (KeyError, TypeError) as exc:
            raise ValueError(
                f"LLM response did not match expected schema: {exc}"
            ) from exc

    # ------------------------------------------------------------------
    # Template loading
    # ------------------------------------------------------------------

    def _load_template(self, template_name: str) -> str:
        """Read a prompt template file from the prompts directory.

        Template names are restricted to alphanumerics, underscores, and
        hyphens to prevent path traversal attacks.

        Args:
            template_name: Filename stem (without ``.txt`` extension).

        Returns:
            The file contents as a UTF-8 string.

        Raises:
            ValueError: If ``template_name`` contains disallowed characters or
                resolves to a path outside ``prompts_dir``.
            FileNotFoundError: If the template file does not exist.
        """
        if not re.fullmatch(r"[a-zA-Z0-9_-]+", template_name):
            raise ValueError(
                f"Invalid template name '{template_name}'. "
                "Only alphanumerics, underscores, and hyphens are allowed."
            )

        template_path = (self._prompts_dir / f"{template_name}.txt").resolve()

        if not template_path.is_relative_to(self._prompts_dir):
            raise ValueError(
                "Resolved template path escapes the prompts directory."
            )

        return template_path.read_text(encoding="utf-8")
