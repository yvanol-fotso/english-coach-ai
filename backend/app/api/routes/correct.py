from fastapi import APIRouter

from app.api.deps import LLM, CurrentUser, Db
from app.repositories import activities
from app.schemas.correct import CorrectionResult, CorrectRequest
from app.services import prompts

router = APIRouter(prefix="/correct", tags=["correct"])


@router.post("", response_model=CorrectionResult)
async def correct(body: CorrectRequest, llm: LLM, db: Db, user: CurrentUser) -> CorrectionResult:
    messages = [
        {"role": "system", "content": prompts.correct_system(body.level, body.ui_language)},
        {"role": "user", "content": body.text},
    ]
    result = await llm.structured(messages, CorrectionResult)
    payload = {"original": body.text, "corrected": result.corrected_text, "issues": len(result.issues)}
    await activities.log(db, user.id, "writing", payload=payload)
    await db.commit()
    return result
