from pydantic import BaseModel, Field

from app.schemas.common import Level, UiLanguage


class ExplainRequest(BaseModel):
    term: str = Field(min_length=1, max_length=200)
    level: Level = "B1"
    ui_language: UiLanguage = "fr"


class Explanation(BaseModel):
    term: str
    part_of_speech: str
    definition: str
    translation: str
    examples: list[str] = []
    pronunciation_tip: str = ""
