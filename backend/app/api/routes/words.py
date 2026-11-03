from fastapi import APIRouter, Response

from app.api.deps import CurrentUser, Db
from app.core.errors import NotFoundError
from app.repositories import words
from app.schemas.explain import Explanation
from app.schemas.history import ReviewGrade, WordOut

router = APIRouter(prefix="/words", tags=["vocabulary"])


@router.get("", response_model=list[WordOut])
async def list_words(db: Db, user: CurrentUser) -> list[WordOut]:
    return [words.to_out(w) for w in await words.list_for(db, user.id)]


@router.get("/review", response_model=list[WordOut])
async def words_to_review(db: Db, user: CurrentUser) -> list[WordOut]:
    return [words.to_out(w) for w in await words.due(db, user.id)]


@router.post("/{word_id}/review", status_code=204)
async def review_word(word_id: int, body: ReviewGrade, db: Db, user: CurrentUser) -> Response:
    if not await words.grade(db, user.id, word_id, body.grade):
        raise NotFoundError()
    await db.commit()
    return Response(status_code=204)


@router.post("", response_model=WordOut, status_code=201)
async def save_word(body: Explanation, db: Db, user: CurrentUser) -> WordOut:
    word = await words.add(db, user.id, body)
    await db.commit()
    return words.to_out(word)


@router.delete("/{word_id}", status_code=204)
async def delete_word(word_id: int, db: Db, user: CurrentUser) -> Response:
    if not await words.remove(db, user.id, word_id):
        raise NotFoundError()
    await db.commit()
    return Response(status_code=204)
