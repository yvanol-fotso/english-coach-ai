from collections.abc import AsyncIterator

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from app import catalog
from app.api.deps import LLM, Config, CurrentUser, Db
from app.api.streaming import ndjson
from app.core.errors import AppError, LLMInvalidOutputError, NotFoundError
from app.repositories import activities, conversations
from app.schemas.chat import ChatRequest
from app.schemas.correct import CorrectionResult
from app.services import prompts

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("")
async def chat(body: ChatRequest, request: Request, llm: LLM, cfg: Config, db: Db, user: CurrentUser) -> StreamingResponse:
    text = body.messages[-1].content
    scenario = catalog.SCENARIO_BY_ID[body.scenario]
    if body.conversation_id:
        conversation = await conversations.get_owned(db, user.id, body.conversation_id)
        if conversation is None:
            raise NotFoundError()
    else:
        first = next(m.content for m in body.messages if m.role == "user")
        title = f"{scenario.label[body.ui_language]}" if body.opening else first
        conversation = await conversations.start(db, user.id, body.scenario, body.level, title, body.target)
    message_id = None
    if not body.opening:
        message_id = (await conversations.add_message(db, conversation, "user", text)).id
    await db.commit()

    conversation_id, title, user_id = conversation.id, conversation.title, user.id
    system = prompts.chat_system(body.scenario, body.level, body.feedback, body.ui_language, body.target, body.opening)
    history = [{"role": m.role, "content": m.content} for m in body.messages[-cfg.max_history_messages :]]
    check = body.feedback == "inline" and not body.opening and len(text.split()) >= 2
    factory = request.app.state.session_factory

    async def events() -> AsyncIterator[str]:
        yield ndjson({"conversation": conversation_id})

        if check:
            messages = [
                {"role": "system", "content": prompts.chat_correction_system(body.level, body.ui_language, body.target)},
                {"role": "user", "content": text},
            ]
            try:
                correction = await llm.structured(messages, CorrectionResult, temperature=0.2)
            except LLMInvalidOutputError:
                correction = None
            except AppError as exc:
                yield ndjson({"error": exc.code})
                return
            if correction:
                async with factory() as session:
                    await conversations.save_correction(session, message_id, correction.model_dump())
                    await session.commit()
                yield ndjson({"correction": correction.model_dump()})

        parts: list[str] = []
        try:
            async for token in llm.stream([{"role": "system", "content": system}, *history]):
                parts.append(token)
                yield ndjson({"token": token})
        except AppError as exc:
            yield ndjson({"error": exc.code})
            return

        reply = "".join(parts).strip()
        if reply:
            async with factory() as session:
                stored = await conversations.get_owned(session, user_id, conversation_id)
                if stored:
                    await conversations.add_message(session, stored, "assistant", reply)
                    await activities.log_speaking(session, user_id, conversation_id, title)
                    await session.commit()
        yield ndjson({"done": True})

    return StreamingResponse(events(), media_type="application/x-ndjson")
