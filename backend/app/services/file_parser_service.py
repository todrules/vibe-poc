"""Service abstraction for parsing uploaded requirement text."""


class FileParserService:
    """Scaffold parser; currently assumes plain text."""

    @staticmethod
    def parse_text(content: str) -> str:
        return content.strip()
