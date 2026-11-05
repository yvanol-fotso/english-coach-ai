"""Checks the installation: python -m app.doctor"""
import asyncio
import importlib.util
import sys

import httpx
from sqlalchemy import text

from app.core.config import get_settings
from app.db.session import create_engine


def report(ok: bool, label: str, hint: str = "") -> bool:
    print(f"[ OK ] {label}" if ok else f"[FAIL] {label}\n       -> {hint}")
    return ok


async def main() -> int:
    settings = get_settings()
    failures = 0
    failures += not report(sys.version_info >= (3, 11), f"Python {sys.version.split()[0]}", "Python 3.11 or newer is required")

    needed = ["fastapi", "uvicorn", "httpx", "pydantic_settings", "multipart", "sqlalchemy", "aiosqlite", "asyncpg"]
    for module in needed:
        found = importlib.util.find_spec(module) is not None
        failures += not report(found, f"package {module}", "run: pip install -r requirements.txt (from the project root)")

    try:
        async with httpx.AsyncClient(base_url=settings.ollama_base_url, timeout=4) as http:
            models = [m["name"] for m in (await http.get("/api/tags")).json().get("models", [])]
        failures += not report(True, f"Ollama reachable at {settings.ollama_base_url}")
        failures += not report(settings.ollama_model in models, f"model {settings.ollama_model} installed", f"run: ollama pull {settings.ollama_model}")
    except Exception:
        failures += not report(False, "Ollama reachable", "open the Ollama app or run: ollama serve")

    engine = create_engine(settings.resolved_database_url)
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        report(True, f"database ({settings.db_mode})")
    except Exception as error:
        failures += not report(False, f"database ({settings.db_mode})", f"{type(error).__name__}: {error}")
    finally:
        await engine.dispose()

    for module, label in (("faster_whisper", "Whisper (optional)"), ("piper", "Piper (optional)")):
        print(f"[ -- ] {label}: {'installed' if importlib.util.find_spec(module) else 'not installed, the browser voice is used'}")

    print("\nAll good." if not failures else f"\n{failures} problem(s) found. Fix the lines marked FAIL.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
