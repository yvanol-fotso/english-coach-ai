from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Conversation, Message, MessageCorrection, utcnow


async def start(db: AsyncSession, user_id: int, scenario: str, level: str, title: str) -> Conversation:
    conversation = Conversation(user_id=user_id, scenario=scenario, level=level, title=title.strip()[:120] or "…")
    db.add(conversation)
    await db.flush()
    return conversation


async def get_owned(db: AsyncSession, user_id: int, conversation_id: int) -> Conversation | None:
    query = select(Conversation).where(Conversation.id == conversation_id, Conversation.user_id == user_id)
    return (await db.execute(query)).scalar_one_or_none()


async def add_message(db: AsyncSession, conversation: Conversation, role: str, content: str) -> Message:
    message = Message(conversation_id=conversation.id, role=role, content=content)
    db.add(message)
    conversation.updated_at = utcnow()
    await db.flush()
    return message


async def save_correction(db: AsyncSession, message_id: int, data: dict) -> None:
    db.add(MessageCorrection(message_id=message_id, data=data))


async def list_for(db: AsyncSession, user_id: int, limit: int = 100) -> list[tuple[Conversation, int]]:
    query = (
        select(Conversation, func.count(Message.id))
        .outerjoin(Message, Message.conversation_id == Conversation.id)
        .where(Conversation.user_id == user_id)
        .group_by(Conversation.id)
        .order_by(Conversation.updated_at.desc())
        .limit(limit)
    )
    return [(c, n) for c, n in (await db.execute(query)).all()]


async def messages_of(db: AsyncSession, conversation_id: int) -> list[tuple[Message, dict | None]]:
    query = (
        select(Message, MessageCorrection.data)
        .outerjoin(MessageCorrection, MessageCorrection.message_id == Message.id)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.id)
    )
    return [(m, c) for m, c in (await db.execute(query)).all()]


async def remove(db: AsyncSession, user_id: int, conversation_id: int) -> bool:
    conversation = await get_owned(db, user_id, conversation_id)
    if conversation is None:
        return False
    ids = select(Message.id).where(Message.conversation_id == conversation_id)
    await db.execute(delete(MessageCorrection).where(MessageCorrection.message_id.in_(ids)))
    await db.execute(delete(Message).where(Message.conversation_id == conversation_id))
    await db.delete(conversation)
    return True
