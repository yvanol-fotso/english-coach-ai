from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.core.errors import register_error_handlers
from app.db.session import create_engine, create_session_factory, init_db
from app.services.ollama import OllamaClient
from app.services.speech import SpeechService

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = create_engine(settings.resolved_database_url)
    await init_db(engine)
    app.state.session_factory = create_session_factory(engine)
    timeout = httpx.Timeout(settings.request_timeout, connect=5.0)
    async with httpx.AsyncClient(base_url=settings.ollama_base_url, timeout=timeout) as http:
        app.state.llm = OllamaClient(http, settings)
        app.state.speech = SpeechService(settings)
        yield
    await engine.dispose()


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
register_error_handlers(app)
app.include_router(api_router, prefix=settings.api_prefix)
