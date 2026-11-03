from typing import Literal

Level = Literal["A0", "A1", "A2", "B1", "B2", "C1", "C2"]
Language = Literal["fr", "en"]
UiLanguage = Literal["fr", "en"]
Skill = Literal[
    "speaking", "pronunciation", "writing", "reading", "listening", "translation", "vocabulary", "grammar", "creative"
]
SKILLS: tuple[str, ...] = (
    "speaking", "pronunciation", "writing", "reading", "listening", "translation", "vocabulary", "grammar", "creative"
)
