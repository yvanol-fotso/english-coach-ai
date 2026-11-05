from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.common import Level, Target, UiLanguage


class AskRequest(BaseModel):
    question: str = Field(min_length=2, max_length=600)
    detail: Literal["short", "full"] = "short"
    level: Level = "B1"
    ui_language: UiLanguage = "fr"
    target: Target = "en"


class QuickAnswer(BaseModel):
    title: str
    rule: str
    examples: list[str] = []
    exceptions: list[str] = []
    watch_out: str = ""
    spoken: str
