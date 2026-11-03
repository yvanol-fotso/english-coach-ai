from collections.abc import AsyncIterator
from typing import Annotated
from urllib.parse import unquote

from fastapi import Depends, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.db.models import User
from app.repositories import users
from app.services.ollama import OllamaClient
from app.services.speech import SpeechService


def get_llm(request: Request) -> OllamaClient:
    return request.app.state.llm


def get_speech(request: Request) -> SpeechService:
    return request.app.state.speech


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    async with request.app.state.session_factory() as session:
        yield session


Db = Annotated[AsyncSession, Depends(get_session)]


async def get_user(db: Db, x_profile: Annotated[str | None, Header()] = None) -> User:
    name = unquote(x_profile or "").strip()[:64] or "default"
    return await users.get_or_create(db, name)


LLM = Annotated[OllamaClient, Depends(get_llm)]
Config = Annotated[Settings, Depends(get_settings)]
Speech = Annotated[SpeechService, Depends(get_speech)]
CurrentUser = Annotated[User, Depends(get_user)]
