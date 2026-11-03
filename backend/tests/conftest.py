import os
import tempfile
from urllib.parse import quote

os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{tempfile.mkdtemp()}/test.db"

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.correct import CorrectionResult, Issue
from app.schemas.drills import DrillSet
from app.schemas.explain import Explanation
from app.schemas.translate import TranslationResult


class FakeLLM:
    async def structured(self, messages, schema, temperature=0.3):
        if schema is Explanation:
            return Explanation(term="run", part_of_speech="verb", definition="to move fast", translation="courir")
        if schema is CorrectionResult:
            issue = Issue(original="I goed", correction="I went", category="grammar", explanation="Passé irrégulier")
            return CorrectionResult(corrected_text="I went home.", issues=[issue], tip="")
        if schema is DrillSet:
            return DrillSet(sentences=["I like coffee.", "She reads every night."])
        return TranslationResult(source_language="fr", target_language="en", translation="Hello")

    async def stream(self, messages, temperature=0.7):
        for token in ("Nice ", "to meet you."):
            yield token

    async def installed_models(self):
        return ["qwen3:4b"]


@pytest.fixture
def client():
    with TestClient(app) as c:
        app.state.llm = FakeLLM()
        yield c


def as_user(name: str) -> dict:
    return {"x-profile": quote(name)}
