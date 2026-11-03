from fastapi import APIRouter

from app.api.deps import LLM
from app.schemas.practice import Exercise, PracticeRequest
from app.services import prompts

router = APIRouter(prefix="/practice", tags=["practice"])


@router.post("", response_model=Exercise)
async def generate(body: PracticeRequest, llm: LLM) -> Exercise:
    topic = body.topic or "a topic from everyday life"
    messages = [
        {"role": "system", "content": prompts.practice_system(body.kind, body.level, body.ui_language)},
        {"role": "user", "content": f"Topic: {topic}"},
    ]
    exercise = await llm.structured(messages, Exercise, temperature=0.8)
    for question in exercise.questions:
        question.answer_index = min(question.answer_index, len(question.choices) - 1)
    return exercise
