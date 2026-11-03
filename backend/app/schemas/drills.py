from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.common import Level


class DrillRequest(BaseModel):
    kind: Literal["pronunciation", "dictation"]
    level: Level = "B1"
    topic: str | None = Field(default=None, max_length=120)
    count: int = Field(default=5, ge=1, le=10)


class DrillSet(BaseModel):
    sentences: list[str] = Field(min_length=1)
