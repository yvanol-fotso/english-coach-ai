import json
import tempfile

from app.core.config import Settings
from tests.conftest import as_user


def lines(response):
    return [json.loads(line) for line in response.text.splitlines()]


def test_health(client):
    body = client.get("/api/v1/health").json()
    assert body["model_ready"] is True and {"stt", "tts"} <= body.keys()


def test_validation(client):
    assert client.post("/api/v1/translate", json={"text": ""}).status_code == 422
    bad = {"messages": [{"role": "user", "content": "Hi"}], "scenario": "nope"}
    assert client.post("/api/v1/chat", json=bad).status_code == 422


def test_database_url_resolution():
    assert Settings(db_mode="sqlite", database_url=None).resolved_database_url.startswith("sqlite+aiosqlite")
    url = Settings(db_mode="postgres", database_url=None, postgres_password="p@ss").resolved_database_url
    assert url == "postgresql+asyncpg://english_coach:p%40ss@localhost:5432/english_coach"


def test_catalog_lists_scenarios_topics_tools(client):
    data = client.get("/api/v1/catalog").json()
    assert {"free", "debate"} <= {s["id"] for s in data["scenarios"]}
    assert data["topics"] and {"poem", "grammar", "email"} <= {t["id"] for t in data["tools"]}


def test_chat_corrects_first_then_replies_and_saves_everything(client):
    h = as_user("Ana")
    body = {"messages": [{"role": "user", "content": "I goed home yesterday"}], "level": "A2"}
    events = lines(client.post("/api/v1/chat", json=body, headers=h))
    kinds = [next(iter(e)) for e in events]
    assert kinds[:2] == ["conversation", "correction"] and kinds[-1] == "done"
    assert "".join(e.get("token", "") for e in events) == "Nice to meet you."

    conv_id = events[0]["conversation"]
    detail = client.get(f"/api/v1/conversations/{conv_id}", headers=h).json()
    assert [m["role"] for m in detail["messages"]] == ["user", "assistant"]
    assert detail["messages"][0]["correction"]["corrected_text"] == "I went home."
    assert client.get(f"/api/v1/conversations/{conv_id}", headers=as_user("Ben")).status_code == 404

    no_check = {**body, "feedback": "off"}
    assert "correction" not in [next(iter(e)) for e in lines(client.post("/api/v1/chat", json=no_check, headers=h))]

    assert client.delete(f"/api/v1/conversations/{conv_id}", headers=h).status_code == 204


def test_studio_tool_streams_and_logs(client):
    h = as_user("Tool")
    r = client.post("/api/v1/tools/poem", json={"input": "the sea", "options": {"style": "haiku"}}, headers=h)
    assert "".join(e.get("token", "") for e in lines(r)) == "Nice to meet you."
    assert client.post("/api/v1/tools/unknown", json={"input": "x"}, headers=h).status_code == 404
    assert client.get("/api/v1/stats", headers=h).json()["by_skill"]["creative"] == 1


def test_drills(client):
    r = client.post("/api/v1/drills", json={"kind": "dictation", "count": 2})
    assert r.json()["sentences"] == ["I like coffee.", "She reads every night."]


def test_activity_stats_words_and_review(client):
    h = as_user("Chloé")
    client.post("/api/v1/translate", json={"text": "Bonjour"}, headers=h)
    client.post("/api/v1/activities", json={"skill": "pronunciation", "score": 80}, headers=h)
    stats = client.get("/api/v1/stats", headers=h).json()
    assert stats["total"] == 2 and stats["streak"] == 1 and len(stats["days"]) == 28

    explanation = client.post("/api/v1/explain", json={"term": "run"}, headers=h).json()
    saved = client.post("/api/v1/words", json=explanation, headers=h).json()
    assert client.post("/api/v1/words", json=explanation, headers=h).json()["id"] == saved["id"]

    assert [w["id"] for w in client.get("/api/v1/words/review", headers=h).json()] == [saved["id"]]
    assert client.post(f"/api/v1/words/{saved['id']}/review", json={"grade": "good"}, headers=h).status_code == 204
    assert client.get("/api/v1/words/review", headers=h).json() == []
    assert client.post(f"/api/v1/words/{saved['id']}/review", json={"grade": "good"}, headers=as_user("X")).status_code == 404

    assert client.delete(f"/api/v1/words/{saved['id']}", headers=h).status_code == 204
    assert client.get("/api/v1/words", headers=h).json() == []


def test_languages_catalog_and_validation(client):
    data = client.get("/api/v1/catalog").json()
    available = {l["code"] for l in data["languages"] if l["available"]}
    assert {"en", "fr", "es"} <= available and "de" not in available
    assert len(data["units"]) >= 8
    bad = {"messages": [{"role": "user", "content": "Hallo"}], "target": "de"}
    assert client.post("/api/v1/chat", json=bad).status_code == 422


def test_chat_in_french_uses_target_language_and_filters_history(client):
    from app.main import app

    h = as_user("Lea")
    body = {"messages": [{"role": "user", "content": "Bonjour, je vais bien"}], "target": "fr", "ui_language": "en"}
    events = lines(client.post("/api/v1/chat", json=body, headers=h))
    assert "Always speak French" in app.state.llm.calls[-1][1] or any("French" in c[1] for c in app.state.llm.calls)
    assert [c["language"] for c in client.get("/api/v1/conversations?language=fr", headers=h).json()] == ["fr"]
    assert client.get("/api/v1/conversations?language=es", headers=h).json() == []


def test_call_opening_has_no_user_message_and_summary_works(client):
    h = as_user("Caller")
    body = {"messages": [{"role": "user", "content": "(call started)"}], "opening": True, "scenario": "meeting"}
    events = lines(client.post("/api/v1/chat", json=body, headers=h))
    assert "correction" not in [next(iter(e)) for e in events]
    conv_id = events[0]["conversation"]
    detail = client.get(f"/api/v1/conversations/{conv_id}", headers=h).json()
    assert [m["role"] for m in detail["messages"]] == ["assistant"]
    summary = client.post(f"/api/v1/conversations/{conv_id}/summary", json={}, headers=h).json()
    assert summary["next_step"] == "Continue."


def test_ask_and_translate_directions(client):
    h = as_user("Asker")
    answer = client.post("/api/v1/ask", json={"question": "Quand utiliser however ?"}, headers=h).json()
    assert answer["spoken"] and client.get("/api/v1/stats", headers=h).json()["by_skill"]["grammar"] == 1
    r = client.post("/api/v1/translate", json={"text": "Hello", "source": "target", "target": "es"}, headers=h)
    assert r.status_code == 200


def test_course_lesson_is_cached_and_progress_tracks(client):
    from app.main import app

    h = as_user("Student")
    units = client.get("/api/v1/course?target=en", headers=h).json()
    assert units[0]["done"] is False
    before = len(app.state.llm.calls)
    for _ in range(2):
        assert client.post("/api/v1/course/hello/lesson", json={"target": "en"}, headers=h).status_code == 200
    assert len(app.state.llm.calls) - before == 1
    assert client.post("/api/v1/course/hello/complete", json={"target": "en", "score": 80}, headers=h).status_code == 204
    done = {u["id"]: u for u in client.get("/api/v1/course?target=en", headers=h).json()}
    assert done["hello"]["done"] and done["hello"]["score"] == 80
    assert not client.get("/api/v1/course?target=fr", headers=h).json()[0]["done"]
    assert client.post("/api/v1/course/nope/lesson", json={}, headers=h).status_code == 404


def test_words_are_separated_by_language(client):
    h = as_user("Poly")
    word = {"term": "pain", "part_of_speech": "noun", "definition": "bread", "translation": "bread", "language": "fr"}
    client.post("/api/v1/words", json=word, headers=h)
    assert len(client.get("/api/v1/words?language=fr", headers=h).json()) == 1
    assert client.get("/api/v1/words?language=en", headers=h).json() == []


def test_old_database_gets_new_columns():
    import asyncio
    import sqlite3

    from app.db.session import create_engine, init_db

    path = tempfile.mkdtemp() + "/old.db"
    db = sqlite3.connect(path)
    db.execute("CREATE TABLE conversations (id INTEGER PRIMARY KEY, user_id INT, scenario VARCHAR(16), level VARCHAR(2), title VARCHAR(120), created_at DATETIME, updated_at DATETIME)")
    db.execute("CREATE TABLE words (id INTEGER PRIMARY KEY, user_id INT, term VARCHAR(200), data JSON, created_at DATETIME)")
    db.commit(); db.close()

    async def run():
        engine = create_engine(f"sqlite+aiosqlite:///{path}")
        await init_db(engine)
        await engine.dispose()

    asyncio.run(run())
    db = sqlite3.connect(path)
    assert "language" in [r[1] for r in db.execute("PRAGMA table_info(conversations)")]
    assert "language" in [r[1] for r in db.execute("PRAGMA table_info(words)")]
