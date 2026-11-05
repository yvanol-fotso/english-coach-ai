from collections.abc import AsyncIterator

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from app import catalog
from app.api.deps import LLM, CurrentUser
from app.api.streaming import ndjson
from app.core.errors import AppError, NotFoundError
from app.repositories import activities
from app.schemas.tools import ToolRequest
from app.services import prompts

router = APIRouter(tags=["studio"])


@router.get("/catalog")
async def get_catalog() -> dict:
    return catalog.public()


@router.post("/tools/{tool_id}")
async def run_tool(tool_id: str, body: ToolRequest, request: Request, llm: LLM, user: CurrentUser) -> StreamingResponse:
    spec = catalog.TOOL_BY_ID.get(tool_id)
    if spec is None:
        raise NotFoundError()

    chosen = {}
    for opt in spec.options:
        allowed = {c.id for c in opt.choices}
        value = body.options.get(opt.id)
        chosen[opt.id] = value if value in allowed else opt.choices[0].id

    messages = [
        {"role": "system", "content": prompts.tool_system(spec, body.level, body.ui_language, body.target, chosen)},
        {"role": "user", "content": body.input},
    ]
    factory, user_id = request.app.state.session_factory, user.id

    async def events() -> AsyncIterator[str]:
        produced = False
        try:
            async for token in llm.stream(messages, temperature=spec.temperature):
                produced = True
                yield ndjson({"token": token})
        except AppError as exc:
            yield ndjson({"error": exc.code})
            return
        if produced:
            async with factory() as session:
                await activities.log(session, user_id, spec.skill, payload={"tool": spec.id, "input": body.input[:200]})
                await session.commit()
        yield ndjson({"done": True})

    return StreamingResponse(events(), media_type="application/x-ndjson")
