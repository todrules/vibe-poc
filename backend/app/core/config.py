"""Application configuration loaded from environment variables."""

import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, Field


class Settings(BaseModel):
    """OptnAI API connection settings sourced from environment variables."""

    optnai_base_url: str = Field(
        description="Base URL for the OptnAI-compatible Chat Completions API."
    )
    optnai_api_key: str = Field(
        description="OptnAI API key."
    )
    optnai_model: str = Field(
        description="Model identifier accepted by OptnAI (e.g. gpt-4o-mini)."
    )

    @classmethod
    def from_env(cls) -> "Settings":
        """Construct settings from environment variables.

        Raises:
            ValueError: If any required environment variable is missing.
        """
        env_values = _load_environment_values()
        missing = [
            key
            for key in ("OPTNAI_BASE_URL", "OPTNAI_API_KEY", "OPTNAI_MODEL")
            if not env_values.get(key)
        ]

        if missing:
            missing_keys = ", ".join(missing)
            raise ValueError(
                "Missing required settings: "
                f"{missing_keys}. Set them as environment variables or in .env."
            )

        return cls(
            optnai_base_url=env_values["OPTNAI_BASE_URL"],
            optnai_api_key=env_values["OPTNAI_API_KEY"],
            optnai_model=env_values["OPTNAI_MODEL"],
        )


def _load_environment_values() -> dict[str, str]:
    """Load runtime configuration from ``.env`` and process environment.

    Values are resolved in the following order:
    1. ``.env`` files (repository root, then backend directory)
    2. Process environment variables (highest priority)

    Returns:
        Mapping of environment variable keys to their resolved values.
    """
    values: dict[str, str] = {}

    for dotenv_path in _candidate_dotenv_paths():
        if dotenv_path.is_file():
            values.update(_parse_dotenv(dotenv_path))

    # Runtime environment always overrides .env file values.
    values.update(dict(os.environ))
    return values


def _candidate_dotenv_paths() -> list[Path]:
    """Return the ordered set of supported ``.env`` file locations."""
    repo_root = Path(__file__).resolve().parents[3]
    backend_root = Path(__file__).resolve().parents[2]

    candidates = [repo_root / ".env", backend_root / ".env"]

    # Keep order stable while removing duplicates.
    unique: list[Path] = []
    for path in candidates:
        if path not in unique:
            unique.append(path)

    return unique


def _parse_dotenv(dotenv_path: Path) -> dict[str, str]:
    """Parse a basic ``.env`` file into a key/value mapping.

    Supports ``KEY=VALUE`` lines and ignores empty lines or comments.
    Surrounding single or double quotes in values are stripped.
    """
    values: dict[str, str] = {}
    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        values[key] = value

    return values


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached singleton of the application settings.

    Using ``lru_cache`` avoids repeated environment reads and makes it
    straightforward to override via dependency injection in tests.
    """
    return Settings.from_env()
