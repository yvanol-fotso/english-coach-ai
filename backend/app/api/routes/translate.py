from fastapi import APIRouter

from app.api.deps import LLM, CurrentUser, Db
from app.repositories import activities
from app.schemas.translate import TranslateRequest, TranslationResult
from app.services import prompts

router = APIRouter(prefix="/translate", tags=["translate"])


@router.post("", response_model=TranslationResult)
async def translate(body: TranslateRequest, llm: LLM, db: Db, user: CurrentUser) -> TranslationResult:
    hint = "" if body.source == "auto" else f"The source language is {body.source}. "
    messages = [
        {"role": "system", "content": prompts.translate_system()},
        {"role": "user", "content": f"{hint}Text:\n{body.text}"},
    ]
    result = await llm.structured(messages, TranslationResult)
    await activities.log(db, user.id, "translation", payload={"original": body.text, "translation": result.translation})
    await db.commit()
    return result
