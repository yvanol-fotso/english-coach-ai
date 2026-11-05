from pathlib import Path

from sqlalchemy import event, inspect, text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.db.base import Base
from app.db import models  # noqa: F401  (registers the tables)


def create_engine(url: str) -> AsyncEngine:
    parsed = make_url(url)
    is_sqlite = parsed.get_backend_name() == "sqlite"
    if is_sqlite and parsed.database and parsed.database != ":memory:":
        Path(parsed.database).parent.mkdir(parents=True, exist_ok=True)

    engine = create_async_engine(url, pool_pre_ping=True)
    if is_sqlite:

        @event.listens_for(engine.sync_engine, "connect")
        def _pragmas(connection, _):
            cursor = connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False)


# Columns added after the first release. Existing databases get them on startup.
COLUMN_MIGRATIONS = (
    ("conversations", "language", "VARCHAR(8) NOT NULL DEFAULT 'en'"),
    ("words", "language", "VARCHAR(8) NOT NULL DEFAULT 'en'"),
)


def _add_missing_columns(connection) -> None:
    inspector = inspect(connection)
    for table, column, ddl in COLUMN_MIGRATIONS:
        if column not in {c["name"] for c in inspector.get_columns(table)}:
            connection.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {ddl}"))


async def init_db(engine: AsyncEngine) -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        await connection.run_sync(_add_missing_columns)
