from fastapi import APIRouter

from app.api.routes import (
    activities, ask, chat, conversations, correct, course, drills, explain, health, me, practice, speech, tools,
    translate, words,
)

api_router = APIRouter()
for module in (
    health, me, chat, conversations, translate, correct, practice, explain, ask, course, words, activities, tools,
    drills, speech
):
    api_router.include_router(module.router)
