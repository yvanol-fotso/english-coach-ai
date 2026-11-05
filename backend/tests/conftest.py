import os
import tempfile
from urllib.parse import quote

os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{tempfile.mkdtemp()}/test.db"

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.ask import QuickAnswer
from app.schemas.correct import CorrectionResult, Issue
from app.schemas.course import CallSummary, DialogueLine, Lesson, Phrase
from app.schemas.drills import DrillSet
from app.schemas.explain import Explanation
from app.schemas.practice import Question
from app.schemas.translate import TranslationResult


class FakeLLM:
    def __init__(self):
        self.calls: list[tuple[str, str]] = []

    async def structured(self, messages, schema, temperature=0.3):
        self.calls.append((schema.__name__, messages[0]["content"]))
        if schema is Explanation:
            return Explanation(term="run", part_of_speech="verb", definition="to move fast", translation="courir")
        if schema is CorrectionResult:
            issue = Issue(original="I goed", correction="I went", category="grammar", explanation="Passé irrégulier")
            return CorrectionResult(corrected_text="I went home.", issues=[issue], tip="")
        if schema is DrillSet:
            return DrillSet(sentences=["I like coffee.", "She reads every night."])
        if schema is QuickAnswer:
            return QuickAnswer(title="However", rule="Contrast.", examples=["It rained. However, we went out."], spoken="Use however to contrast.")
        if schema is Lesson:
            q = Question(question="Que veut dire hello ?", choices=["Bonjour", "Merci"], answer_index=0, explanation="Salut.")
            return Lesson(
                title="Dire bonjour", intro="Saluer.", tip="",
                phrases=[Phrase(text="Hello", meaning="Bonjour")] * 3,
                dialogue=[DialogueLine(speaker="A", text="Hello", meaning="Bonjour")] * 2,
                quiz=[q, q],
            )
        if schema is CallSummary:
            return CallSummary(summary="Bien.", phrases=["I went"], next_step="Continue.")
        return TranslationResult(source_language="fr", target_language="en", translation="Hello")

    async def stream(self, messages, temperature=0.7):
        self.calls.append(("stream", messages[0]["content"]))
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
