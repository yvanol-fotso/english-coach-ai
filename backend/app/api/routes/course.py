from fastapi import APIRouter, Query, Response

from app import catalog
from app.api.deps import LLM, CurrentUser, Db
from app.core.errors import NotFoundError
from app.repositories import activities, course
from app.schemas.common import Target
from app.schemas.course import CompleteRequest, Lesson, LessonRequest, UnitProgress
from app.services import prompts

router = APIRouter(prefix="/course", tags=["course"])


@router.get("", response_model=list[UnitProgress])
async def get_course(db: Db, user: CurrentUser, target: Target = Query("en")) -> list[UnitProgress]:
    done = await course.progress(db, user.id, target)
    return [UnitProgress(id=u.id, done=u.id in done, score=done.get(u.id)) for u in catalog.UNITS]


@router.post("/{unit_id}/lesson", response_model=Lesson)
async def get_lesson(unit_id: str, body: LessonRequest, llm: LLM, db: Db) -> Lesson:
    unit = catalog.UNIT_BY_ID.get(unit_id)
    if unit is None:
        raise NotFoundError()
    cached = await course.cached_lesson(db, body.target, unit_id, body.ui_language)
    if cached:
        return Lesson(**cached)
    messages = [
        {"role": "system", "content": prompts.lesson_system(unit, body.ui_language, body.target)},
        {"role": "user", "content": f"Unit: {unit.topic}"},
    ]
    lesson = await llm.structured(messages, Lesson, temperature=0.5)
    for question in lesson.quiz:
        question.answer_index = min(question.answer_index, len(question.choices) - 1)
    await course.save_lesson(db, body.target, unit_id, body.ui_language, lesson.model_dump())
    await db.commit()
    return lesson


@router.post("/{unit_id}/complete", status_code=204)
async def complete(unit_id: str, body: CompleteRequest, db: Db, user: CurrentUser) -> Response:
    if unit_id not in catalog.UNIT_BY_ID:
        raise NotFoundError()
    await course.complete(db, user.id, body.target, unit_id, body.score)
    await activities.log(db, user.id, "course", score=body.score, payload={"unit": unit_id, "language": body.target})
    await db.commit()
    return Response(status_code=204)
