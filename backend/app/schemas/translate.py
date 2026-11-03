from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.common import Language


class TranslateRequest(BaseModel):
    text: str = Field(min_length=1, max_length=4000)
    source: Literal["auto", "fr", "en"] = "auto"


class TranslationResult(BaseModel):
    source_language: Language
    target_language: Language
    translation: str
    alternatives: list[str] = []
