from pydantic import BaseModel, Field

from app.schemas.common import Level, Target, UiLanguage


class ToolRequest(BaseModel):
    input: str = Field(min_length=1, max_length=4000)
    options: dict[str, str] = {}
    level: Level = "B1"
    ui_language: UiLanguage = "fr"
    target: Target = "en"
