from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.common import Level, Target, UiLanguage


class CorrectRequest(BaseModel):
    text: str = Field(min_length=1, max_length=4000)
    level: Level = "B1"
    ui_language: UiLanguage = "fr"
    target: Target = "en"


class Issue(BaseModel):
    original: str
    correction: str
    category: Literal["grammar", "vocabulary", "spelling", "punctuation", "style"]
    explanation: str


class CorrectionResult(BaseModel):
    corrected_text: str
    issues: list[Issue] = []
    tip: str = ""
