from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import LessonCache, LessonProgress, utcnow


async def cached_lesson(db: AsyncSession, language: str, unit_id: str, ui: str) -> dict | None:
    query = select(LessonCache.data).where(
        LessonCache.language == language, LessonCache.unit_id == unit_id, LessonCache.ui_language == ui
    )
    return (await db.execute(query)).scalar_one_or_none()


async def save_lesson(db: AsyncSession, language: str, unit_id: str, ui: str, data: dict) -> None:
    db.add(LessonCache(language=language, unit_id=unit_id, ui_language=ui, data=data))


async def progress(db: AsyncSession, user_id: int, language: str) -> dict[str, int]:
    query = select(LessonProgress.unit_id, LessonProgress.score).where(
        LessonProgress.user_id == user_id, LessonProgress.language == language
    )
    return {unit: score for unit, score in (await db.execute(query)).all()}


async def complete(db: AsyncSession, user_id: int, language: str, unit_id: str, score: int) -> None:
    query = select(LessonProgress).where(
        LessonProgress.user_id == user_id, LessonProgress.language == language, LessonProgress.unit_id == unit_id
    )
    row = (await db.execute(query)).scalar_one_or_none()
    if row is None:
        db.add(LessonProgress(user_id=user_id, language=language, unit_id=unit_id, score=score))
    else:
        row.score, row.completed_at = max(row.score, score), utcnow()
