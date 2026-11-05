from fastapi import APIRouter

from app.api.deps import LLM, CurrentUser, Db
from app.repositories import activities
from app.schemas.ask import AskRequest, QuickAnswer
from app.services import prompts

router = APIRouter(prefix="/ask", tags=["ask"])


@router.post("", response_model=QuickAnswer)
async def ask(body: AskRequest, llm: LLM, db: Db, user: CurrentUser) -> QuickAnswer:
    messages = [
        {"role": "system", "content": prompts.ask_system(body.level, body.ui_language, body.target, body.detail)},
        {"role": "user", "content": body.question},
    ]
    answer = await llm.structured(messages, QuickAnswer, temperature=0.3)
    await activities.log(db, user.id, "grammar", payload={"question": body.question[:160]})
    await db.commit()
    return answer
