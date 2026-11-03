import asyncio
import json
from collections.abc import AsyncIterator
from typing import TypeVar

import httpx
from pydantic import BaseModel, ValidationError

from app.core.config import Settings
from app.core.errors import LLMInvalidOutputError, LLMUnavailableError

T = TypeVar("T", bound=BaseModel)


class OllamaClient:
    def __init__(self, http: httpx.AsyncClient, settings: Settings) -> None:
        self._http = http
        self._cfg = settings
        self._gate = asyncio.Semaphore(settings.max_concurrent_generations)

    def _payload(self, messages: list[dict], *, stream: bool, fmt: dict | None = None, temperature: float = 0.7) -> dict:
        payload = {
            "model": self._cfg.ollama_model,
            "messages": messages,
            "stream": stream,
            "think": False,
            "keep_alive": self._cfg.ollama_keep_alive,
            "options": {"temperature": temperature, "num_ctx": self._cfg.num_ctx},
        }
        if fmt:
            payload["format"] = fmt
        return payload

    async def stream(self, messages: list[dict], temperature: float = 0.7) -> AsyncIterator[str]:
        async with self._gate:
            try:
                async with self._http.stream("POST", "/api/chat", json=self._payload(messages, stream=True, temperature=temperature)) as resp:
                    resp.raise_for_status()
                    async for line in resp.aiter_lines():
                        if not line:
                            continue
                        chunk = json.loads(line)
                        if token := chunk.get("message", {}).get("content"):
                            yield token
                        if chunk.get("done"):
                            return
            except httpx.HTTPError as exc:
                raise LLMUnavailableError from exc

    async def structured(self, messages: list[dict], schema: type[T], temperature: float = 0.3) -> T:
        payload = self._payload(messages, stream=False, fmt=schema.model_json_schema(), temperature=temperature)
        async with self._gate:
            try:
                resp = await self._http.post("/api/chat", json=payload)
                resp.raise_for_status()
            except httpx.HTTPError as exc:
                raise LLMUnavailableError from exc
        try:
            return schema.model_validate_json(resp.json()["message"]["content"])
        except (ValidationError, KeyError, ValueError) as exc:
            raise LLMInvalidOutputError from exc

    async def installed_models(self) -> list[str]:
        try:
            resp = await self._http.get("/api/tags", timeout=3)
            resp.raise_for_status()
        except httpx.HTTPError:
            return []
        return [m["name"] for m in resp.json().get("models", [])]
