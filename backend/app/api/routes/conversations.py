from fastapi import APIRouter, Response

from app.api.deps import CurrentUser, Db
from app.core.errors import NotFoundError
from app.repositories import conversations
from app.schemas.correct import CorrectionResult
from app.schemas.history import ConversationDetail, ConversationSummary, MessageOut

router = APIRouter(prefix="/conversations", tags=["history"])


@router.get("", response_model=list[ConversationSummary])
async def list_conversations(db: Db, user: CurrentUser) -> list[ConversationSummary]:
    rows = await conversations.list_for(db, user.id)
    return [
        ConversationSummary(
            id=c.id, title=c.title, scenario=c.scenario, level=c.level, updated_at=c.updated_at, message_count=n
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
