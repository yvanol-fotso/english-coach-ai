from pydantic import BaseModel, Field

from app.schemas.common import Target, UiLanguage
from app.schemas.practice import Question


class Phrase(BaseModel):
    text: str
    meaning: str
    tip: str = ""


class DialogueLine(BaseModel):
    speaker: str
    text: str
    meaning: str


class Lesson(BaseModel):
    title: str
    intro: str
    phrases: list[Phrase] = Field(min_length=3)
    dialogue: list[DialogueLine] = Field(min_length=2)
    quiz: list[Question] = Field(min_length=2)
    tip: str = ""


class LessonRequest(BaseModel):
    target: Target = "en"
    ui_language: UiLanguage = "fr"


class CompleteRequest(BaseModel):
    target: Target = "en"
    score: int = Field(ge=0, le=100)


class UnitProgress(BaseModel):
    id: str
    done: bool
    score: int | None = None


class SummaryRequest(BaseModel):
    ui_language: UiLanguage = "fr"


class CallMistake(BaseModel):
    wrong: str
    right: str
    why: str


class CallSummary(BaseModel):
    summary: str
    mistakes: list[CallMistake] = []
    phrases: list[str] = []
    next_step: str
