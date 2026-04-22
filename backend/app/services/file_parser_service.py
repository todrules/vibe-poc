"""Service for normalising and merging user-supplied requirement text."""


class FileParserService:
    """Handles pre-processing of free-form text before it is sent to the LLM.

    The service is intentionally stateless so it can be used as a singleton
    or instantiated per-request without side effects.
    """

    @staticmethod
    def merge(requirements: str, file_text: str | None = None) -> str:
        """Merge typed requirements with optional uploaded file text.

        Both inputs are stripped of leading and trailing whitespace.  When
        ``file_text`` is present it is appended to ``requirements`` under a
        clearly labelled heading so the LLM can distinguish the two sources.

        Args:
            requirements: Free-form requirement text entered by the user.
            file_text: Optional supplementary text extracted from an uploaded
                file.  Pass ``None`` or an empty string to ignore.

        Returns:
            A single normalised string ready for use in an LLM prompt.

        Raises:
            ValueError: If ``requirements`` is empty after stripping.
        """
        base = requirements.strip()
        if not base:
            raise ValueError("requirements must not be empty.")

        if file_text and file_text.strip():
            base = f"{base}\n\n--- Uploaded file content ---\n{file_text.strip()}"

        return base
