from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.common import Level, Target, UiLanguage


class PracticeRequest(BaseModel):
    kind: Literal["reading", "listening"]
    level: Level = "B1"
    topic: str | None = Field(default=None, max_length=120)
    ui_language: UiLanguage = "fr"
    target: Target = "en"


class Question(BaseModel):
    question: str
    choices: list[str] = Field(min_length=2, max_length=5)
    answer_index: int = Field(ge=0)
    explanation: str


class Exercise(BaseModel):
    title: str
    passage: str
    questions: list[Question] = Field(min_length=1)
