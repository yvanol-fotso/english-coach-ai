from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

from app.catalog import SCENARIO_BY_ID
from app.schemas.common import Level, Target, UiLanguage


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=4000)


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_length=1)
    conversation_id: int | None = None
    scenario: str = "free"
    level: Level = "B1"
    feedback: Literal["inline", "off"] = "inline"
    ui_language: UiLanguage = "fr"
    target: Target = "en"
    opening: bool = False

    @field_validator("scenario")
    @classmethod
    def known_scenario(cls, value: str) -> str:
        if value not in SCENARIO_BY_ID:
            raise ValueError("unknown scenario")
        return value

    @model_validator(mode="after")
    def last_is_user(self) -> "ChatRequest":
        if self.opening and len(self.messages) != 1:
            raise ValueError("an opening request carries one placeholder message")
        if self.messages[-1].role != "user":
            raise ValueError("the last message must come from the user")
        return self
