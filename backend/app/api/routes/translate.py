from fastapi import APIRouter

from app import catalog
from app.api.deps import LLM, CurrentUser, Db
from app.repositories import activities
from app.schemas.translate import TranslateRequest, TranslationResult
from app.services import prompts

router = APIRouter(prefix="/translate", tags=["translate"])


@router.post("", response_model=TranslationResult)
async def translate(body: TranslateRequest, llm: LLM, db: Db, user: CurrentUser) -> TranslationResult:
    native = body.ui_language if body.ui_language != body.target else ("fr" if body.target != "fr" else "en")
    names = catalog.LANGUAGE_BY_ID
    hint = {
        "auto": "",
        "native": f"The text is in {names[native].name}. ",
        "target": f"The text is in {names[body.target].name}. ",
    }[body.source]
    messages = [
        {"role": "system", "content": prompts.translate_system(native, body.target)},
        {"role": "user", "content": f"{hint}Text:\n{body.text}"},
    ]
    result = await llm.structured(messages, TranslationResult)
    await activities.log(db, user.id, "translation", payload={"original": body.text, "translation": result.translation})
    await db.commit()
    return result
