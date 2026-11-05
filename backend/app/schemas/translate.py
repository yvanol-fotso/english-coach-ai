from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.common import Language, Target, UiLanguage


class TranslateRequest(BaseModel):
    text: str = Field(min_length=1, max_length=4000)
    source: Literal["auto", "native", "target"] = "auto"
    target: Target = "en"
    ui_language: UiLanguage = "fr"


class TranslationResult(BaseModel):
    source_language: Language
    target_language: Language
    translation: str
    alternatives: list[str] = []
