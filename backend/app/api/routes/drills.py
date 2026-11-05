from fastapi import APIRouter

from app.api.deps import LLM
from app.schemas.drills import DrillRequest, DrillSet
from app.services import prompts

router = APIRouter(prefix="/drills", tags=["drills"])


@router.post("", response_model=DrillSet)
async def drills(body: DrillRequest, llm: LLM) -> DrillSet:
    topic = body.topic or "everyday life"
    messages = [
        {"role": "system", "content": prompts.drill_system(body.kind, body.level, body.count, body.target)},
        {"role": "user", "content": f"Topic: {topic}"},
    ]
    result = await llm.structured(messages, DrillSet, temperature=0.8)
    result.sentences = [s.strip() for s in result.sentences if s.strip()][: body.count]
    return result
