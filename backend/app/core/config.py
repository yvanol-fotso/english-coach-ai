from functools import lru_cache
from typing import Literal
from urllib.parse import quote

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "English Coach AI"
    api_prefix: str = "/api/v1"
    cors_origins: list[str] = ["http://localhost:5173"]

    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "qwen3:4b"
    ollama_keep_alive: str = "30m"
    num_ctx: int = 4096
    request_timeout: float = 120.0
    max_concurrent_generations: int = 2

    max_history_messages: int = 20

    db_mode: Literal["sqlite", "postgres"] = "sqlite"
    sqlite_path: str = "data/english_coach.db"
    postgres_user: str = "english_coach"
    postgres_password: str = "english_coach"
    postgres_db: str = "english_coach"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    database_url: str | None = None

    whisper_model: str = "small"
    whisper_device: str = "auto"
    whisper_compute_type: str = "default"
    piper_voice_path: str = "models/piper/en_US-lessac-medium.onnx"
    max_audio_bytes: int = 15 * 1024 * 1024

    @property
    def resolved_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        if self.db_mode == "postgres":
            user, password = quote(self.postgres_user), quote(self.postgres_password)
            return f"postgresql+asyncpg://{user}:{password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        return f"sqlite+aiosqlite:///./{self.sqlite_path}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
