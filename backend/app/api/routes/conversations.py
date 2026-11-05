from fastapi import APIRouter, Query, Response

from app.api.deps import LLM, CurrentUser, Db
from app.core.errors import NotFoundError
from app.repositories import conversations
from app.schemas.correct import CorrectionResult
from app.schemas.course import CallSummary, SummaryRequest
from app.services import prompts
from app.schemas.history import ConversationDetail, ConversationSummary, MessageOut

router = APIRouter(prefix="/conversations", tags=["history"])


@router.get("", response_model=list[ConversationSummary])
async def list_conversations(db: Db, user: CurrentUser, language: str | None = Query(None, max_length=8)) -> list[ConversationSummary]:
    rows = await conversations.list_for(db, user.id, language)
    return [
        ConversationSummary(
            id=c.id, title=c.title, scenario=c.scenario, level=c.level, language=c.language,
            updated_at=c.updated_at, message_count=n
        )
        for c, n in rows
    ]


@router.get("/{conversation_id}", response_model=ConversationDetail)
async def get_conversation(conversation_id: int, db: Db, user: CurrentUser) -> ConversationDetail:
    conversation = await conversations.get_owned(db, user.id, conversation_id)
    if conversation is None:
        raise NotFoundError()
    messages = await conversations.messages_of(db, conversation_id)
    return ConversationDetail(
        id=conversation.id,
        title=conversation.title,
        scenario=conversation.scenario,
        level=conversation.level,
        language=conversation.language,
        updated_at=conversation.updated_at,
        message_count=len(messages),
        messages=[
            MessageOut(
                role=m.role,
                content=m.content,
                created_at=m.created_at,
                correction=CorrectionResult(**c) if c else None,
            )
            for m, c in messages
        ],
    )


@router.delete("/{conversation_id}", status_code=204)
async def delete_conversation(conversation_id: int, db: Db, user: CurrentUser) -> Response:
    if not await conversations.remove(db, user.id, conversation_id):
        raise NotFoundError()
    await db.commit()
    return Response(status_code=204)


@router.post("/{conversation_id}/summary", response_model=CallSummary)
async def summarize(conversation_id: int, body: SummaryRequest, llm: LLM, db: Db, user: CurrentUser) -> CallSummary:
    conversation = await conversations.get_owned(db, user.id, conversation_id)
    if conversation is None:
        raise NotFoundError()
    lines = []
    for message, correction in await conversations.messages_of(db, conversation_id):
        if message.role == "assistant":
            lines.append(f"Coach: {message.content}")
            continue
        lines.append(f"Learner: {message.content}")
        for issue in (correction or {}).get("issues", []):
            lines.append(f"  mistake: {issue['original']} -> {issue['correction']} ({issue['explanation']})")
    messages = [
        {"role": "system", "content": prompts.summary_system(body.ui_language, conversation.language)},
        {"role": "user", "content": "\n".join(lines)[-6000:]},
    ]
    return await llm.structured(messages, CallSummary, temperature=0.3)
