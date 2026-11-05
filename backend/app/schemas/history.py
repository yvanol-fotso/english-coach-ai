from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.common import Skill
from app.schemas.correct import CorrectionResult
from app.schemas.explain import Explanation


class Profile(BaseModel):
    name: str
    created_at: datetime


class ConversationSummary(BaseModel):
    id: int
    title: str
    scenario: str
    level: str
    language: str = "en"
    updated_at: datetime
    message_count: int


class MessageOut(BaseModel):
    role: str
    content: str
    created_at: datetime
    correction: CorrectionResult | None = None


class ConversationDetail(ConversationSummary):
    messages: list[MessageOut]


class ActivityIn(BaseModel):
    skill: Skill
    score: int | None = Field(default=None, ge=0, le=100)
    payload: dict | None = None


class ActivityOut(BaseModel):
    id: int
    skill: str
    score: int | None
    payload: dict | None
    created_at: datetime


class DayCount(BaseModel):
    day: str
    count: int


class Stats(BaseModel):
    total: int
    streak: int
    by_skill: dict[str, int]
    days: list[DayCount]


class WordIn(Explanation):
    language: str = "en"


class WordOut(WordIn):
    id: int
    created_at: datetime


class ReviewGrade(BaseModel):
    grade: Literal["again", "hard", "good", "easy"]
