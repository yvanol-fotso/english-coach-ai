from datetime import UTC, datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


def utcnow() -> datetime:
    return datetime.now(UTC)


def _timestamp() -> Mapped[datetime]:
    return mapped_column(DateTime(timezone=True), default=utcnow)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = _timestamp()


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    scenario: Mapped[str] = mapped_column(String(16))
    level: Mapped[str] = mapped_column(String(2))
    title: Mapped[str] = mapped_column(String(120))
    created_at: Mapped[datetime] = _timestamp()
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"), index=True)
    role: Mapped[str] = mapped_column(String(16))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = _timestamp()


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    skill: Mapped[str] = mapped_column(String(16))
    score: Mapped[int | None] = mapped_column(default=None)
    ref_id: Mapped[int | None] = mapped_column(default=None)
    payload: Mapped[dict | None] = mapped_column(JSON, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)


class Word(Base):
    __tablename__ = "words"
    __table_args__ = (UniqueConstraint("user_id", "term"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    term: Mapped[str] = mapped_column(String(200))
    data: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = _timestamp()


class MessageCorrection(Base):
    __tablename__ = "message_corrections"

    message_id: Mapped[int] = mapped_column(ForeignKey("messages.id"), primary_key=True)
    data: Mapped[dict] = mapped_column(JSON)


class WordReview(Base):
    __tablename__ = "word_reviews"

    word_id: Mapped[int] = mapped_column(ForeignKey("words.id"), primary_key=True)
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    interval_days: Mapped[int] = mapped_column(Integer, default=0)
    ease: Mapped[float] = mapped_column(Float, default=2.5)
    reps: Mapped[int] = mapped_column(Integer, default=0)
