from typing import Annotated, Literal

from pydantic import AfterValidator

from app.catalog import LANGUAGE_BY_ID

Level = Literal["A0", "A1", "A2", "B1", "B2", "C1", "C2"]
UiLanguage = Literal["fr", "en"]
Language = str
Skill = Literal[
    "speaking", "pronunciation", "writing", "reading", "listening", "translation", "vocabulary", "grammar", "creative", "course"
]
SKILLS: tuple[str, ...] = (
    "speaking", "pronunciation", "writing", "reading", "listening", "translation", "vocabulary", "grammar", "creative", "course"
)


def _available(code: str) -> str:
    language = LANGUAGE_BY_ID.get(code)
    if language is None or not language.available:
        raise ValueError("language not available")
    return code


Target = Annotated[str, AfterValidator(_available)]
