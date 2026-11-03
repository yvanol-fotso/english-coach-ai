import json

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
