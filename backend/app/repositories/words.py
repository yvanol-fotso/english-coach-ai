from datetime import timedelta

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Word, WordReview, utcnow
from app.schemas.explain import Explanation
from app.schemas.history import WordOut


def to_out(word: Word) -> WordOut:
    return WordOut(id=word.id, created_at=word.created_at, **word.data)


async def list_for(db: AsyncSession, user_id: int) -> list[Word]:
    query = select(Word).where(Word.user_id == user_id).order_by(Word.created_at.desc())
    return list((await db.execute(query)).scalars())


async def add(db: AsyncSession, user_id: int, explanation: Explanation) -> Word:
    query = select(Word).where(Word.user_id == user_id, Word.term == explanation.term)
    existing = (await db.execute(query)).scalar_one_or_none()
    if existing:
        return existing
    word = Word(user_id=user_id, term=explanation.term, data=explanation.model_dump())
    db.add(word)
    await db.flush()
    return word


async def remove(db: AsyncSession, user_id: int, word_id: int) -> bool:
    owned = select(Word.id).where(Word.id == word_id, Word.user_id == user_id)
    if (await db.execute(owned)).scalar_one_or_none() is None:
        return False
    await db.execute(delete(WordReview).where(WordReview.word_id == word_id))
    await db.execute(delete(Word).where(Word.id == word_id))
    return True


async def due(db: AsyncSession, user_id: int, limit: int = 20) -> list[Word]:
    query = (
        select(Word)
        .outerjoin(WordReview, WordReview.word_id == Word.id)
        .where(Word.user_id == user_id, (WordReview.word_id.is_(None)) | (WordReview.due_at <= utcnow()))
        .order_by(Word.created_at)
        .limit(limit)
    )
    return list((await db.execute(query)).scalars())


async def grade(db: AsyncSession, user_id: int, word_id: int, grade_name: str) -> bool:
    owned = select(Word.id).where(Word.id == word_id, Word.user_id == user_id)
    if (await db.execute(owned)).scalar_one_or_none() is None:
        return False
    review = await db.get(WordReview, word_id)
    if review is None:
        review = WordReview(word_id=word_id, due_at=utcnow(), interval_days=0, ease=2.5, reps=0)
        db.add(review)

    if grade_name == "again":
        review.reps, review.interval_days = 0, 0
        review.ease = max(1.3, review.ease - 0.2)
        review.due_at = utcnow() + timedelta(minutes=10)
        return True

    if grade_name == "hard":
        review.interval_days = max(1, round(review.interval_days * 1.2))
        review.ease = max(1.3, review.ease - 0.15)
    elif grade_name == "good":
        review.interval_days = 1 if review.reps == 0 else 3 if review.reps == 1 else round(review.interval_days * review.ease)
    else:
        review.interval_days = max(4, round(max(review.interval_days, 1) * review.ease * 1.3))
        review.ease += 0.15
    review.reps += 1
    review.due_at = utcnow() + timedelta(days=review.interval_days)
    return True
