# Backend

FastAPI service: it turns learner requests into prompts for Ollama, stores history and progress, and returns validated results.

## Run

```bash
# from the project root: python -m venv .venv, activate it, then
pip install -r requirements.txt
cd backend
cp .env.example .env
uvicorn app.main:app --reload
python -m app.doctor          # checks Python, packages, Ollama, model and database
```

Interactive docs: http://127.0.0.1:8000/docs

## Profiles

Every request may carry an `X-Profile` header (URL-encoded first name). The frontend proxy adds it from a cookie. Without it, the profile is `default`. Data is always filtered by profile.

## Endpoints (prefix `/api/v1`)

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/health` | Server, Ollama, model, Whisper and Piper status |
| GET | `/me` | Current profile |
| GET | `/catalog` | Topics, situations and Studio tools (bilingual labels) |
| POST | `/chat` | `opening: true` makes the coach speak first (calls). Streams `conversation`, then `correction`, then reply tokens (NDJSON); saves everything |
| POST | `/ask` | Short structured answer to a language question (rule, examples, exceptions, spoken version) |
| GET | `/course?target=en` | Course units with the learner's progress |
| POST | `/course/{unit}/lesson`, `/course/{unit}/complete` | A cached beginner lesson; record a completed lesson |
| POST | `/conversations/{id}/summary` | Review of a call: mistakes, phrases, next step |
| POST | `/tools/{id}` | Runs a Studio tool, streams the result, logs the activity |
| POST | `/drills` | Sentences for pronunciation or dictation |
| GET, DELETE | `/conversations`, `/conversations/{id}` | List, reopen, delete conversations |
| POST | `/translate` | FR/EN translation |
| POST | `/correct` | Corrections with explanations |
| POST | `/practice` | Reading or listening exercise with quiz |
| POST | `/explain` | Explain a word or expression |
| GET, POST, DELETE | `/words`, `/words/{id}` | Saved vocabulary |
| GET, POST | `/words/review`, `/words/{id}/review` | Words due for review, grade a review (again, hard, good, easy) |
| GET, POST | `/activities` | Activity feed, log a quiz result |
| GET | `/stats?tz_offset=60` | Streak, totals per skill, last 28 days |
| POST | `/speech/transcribe`, `/speech/synthesize` | Whisper and Piper (optional) |

Chat stream lines: `{"conversation": id}`, `{"correction": {...}}` (when corrections are on), many `{"token": "..."}`, then `{"done": true}` or `{"error": "<code>"}`. The correction of the learner's sentence always comes before the reply.

Errors are JSON: `{"code": "llm_unavailable", "detail": "..."}`. The frontend turns each code into a clear message. Codes: `llm_unavailable`, `llm_bad_output`, `speech_unavailable`, `audio_too_large`, `not_found`.

## Layout

```
app/
  main.py            app factory, lifespan, CORS
  catalog/           languages, course units, scenarios, topics, Studio tools: add an entry to add a feature
  core/              settings (.env) and error types
  db/                SQLAlchemy base, models, engine and sessions
  repositories/      queries: users, conversations, activities, words
  schemas/           Pydantic request and response models
  services/          ollama.py (client), speech.py, prompts.py
  api/               router, dependencies, one module per route
tests/
```

## Database

Async SQLAlchemy 2. `DB_MODE=sqlite` (default) or `DB_MODE=postgres` with the `POSTGRES_*` variables; start Postgres with `docker compose up -d db` at the repository root (the driver is already in `requirements.txt`). `DATABASE_URL` overrides both. Tables are created at startup, and the few columns added after the first release (`language`) are added to an existing database automatically. Add Alembic before making further schema changes.

## Talking to Ollama

`services/ollama.py` keeps one shared `httpx.AsyncClient`.

- `stream()` yields tokens from `/api/chat`.
- `structured()` sends the Pydantic JSON schema as Ollama's `format`, then validates the answer again.
- `think: false` turns off Qwen3's reasoning mode for faster replies.
- A semaphore limits simultaneous generations (`MAX_CONCURRENT_GENERATIONS`).

`services/prompts.py` builds every prompt (conversation, correction of the learner's sentence, Studio tools, drills) from the catalog, the level rules (A0 to C2) and the help language. Scenario and tool texts live in `catalog/`.

## Environment variables

| Variable | Default | Role |
| --- | --- | --- |
| `OLLAMA_BASE_URL` | `http://127.0.0.1:11434` | Ollama server |
| `OLLAMA_MODEL` | `qwen3:4b` | Model name |
| `OLLAMA_KEEP_ALIVE` | `30m` | How long the model stays in VRAM |
| `NUM_CTX` | `4096` | Context window |
| `REQUEST_TIMEOUT` | `120` | Seconds |
| `MAX_CONCURRENT_GENERATIONS` | `2` | Parallel generations |
| `DB_MODE` | `sqlite` | `sqlite` or `postgres` |
| `SQLITE_PATH`, `POSTGRES_*` | see `.env.example` | Database location and credentials |
| `DATABASE_URL` | empty | Full URL, overrides `DB_MODE` |
| `WHISPER_MODEL`, `WHISPER_DEVICE` | `small`, `auto` | Speech to text |
| `PIPER_VOICE_PATH` | `models/piper/en_US-lessac-medium.onnx` | Voice file |
| `CORS_ORIGINS` | `["http://localhost:5173"]` | Allowed origins (JSON list) |

## Speech (optional)

`requirements-speech.txt` (project root) installs `faster-whisper` and `piper-tts`. Both load on first use. If one is missing the route answers `501` with code `speech_unavailable`, and the frontend falls back to the browser.

## Tests

```bash
pytest
```

## Adding an endpoint

A text tool, a situation, a topic, a course unit or a language needs no code: edit `catalog/`. Every request carries `target` (the language being learned) and `ui_language` (the language of explanations). For a new kind of endpoint:

1. Schemas in `schemas/`, prompt in `services/prompts.py`.
2. Route in `api/routes/`, registered in `api/router.py`.
3. Proxy in `frontend/src/routes/api/<name>/+server.ts`.
