from fastapi import APIRouter

from app.api.deps import LLM, CurrentUser, Db
from app.repositories import activities
from app.schemas.explain import Explanation, ExplainRequest
from app.services import prompts

router = APIRouter(prefix="/explain", tags=["vocabulary"])


@router.post("", response_model=Explanation)
async def explain(body: ExplainRequest, llm: LLM, db: Db, user: CurrentUser) -> Explanation:
    messages = [
        {"role": "system", "content": prompts.explain_system(body.level, body.ui_language, body.target)},
        {"role": "user", "content": body.term},
    ]
    result = await llm.structured(messages, Explanation)
    await activities.log(db, user.id, "vocabulary", payload={"term": result.term})
    await db.commit()
    return result
