# English Coach AI

A private English tutor that runs on your own computer. No subscription, no paid API, and your conversations stay on your machine.

Talk out loud, get corrected, hear the answer, and keep going. It works from absolute beginner (A0) to near-native (C2), and the interface is available in French and English.

## What it does

| | |
| --- | --- |
| **Talk** | Free conversation about anything (your day, news, politics, sport, a first meeting). In **voice conversation** mode you speak, the coach corrects your sentence first, then answers out loud, and listens again. Situations: meeting someone, everyday life, PhD or job interview, debate, presenting your work, science talk. |
| **Voice drills** | Pronunciation (say a sentence, get a word-by-word score) and dictation (listen, write, get checked). |
| **Write** | Paste an English text, get a corrected version with each mistake explained. |
| **Understand** | Reading or listening exercises at your level, followed by a quiz. |
| **Studio** | Poems, short stories, rewriting in another tone, grammar lessons, idioms, emails and letters, text simplifying, interview preparation, 60-second pitch. |
| **Translate** | French and English, both ways, with alternatives. |
| **Vocabulary** | Explain any word, hear it, save it, and review it with spaced repetition. |
| **History and progress** | Every conversation is saved and can be reopened. Daily streak and activity per skill. |
| **Settings** | Light, dark or automatic theme, four accent colors, app language, level, voice, profiles. |

## How it fits together

```
Browser ── SvelteKit (pages + proxies) ── FastAPI ── Ollama (Qwen3)
                                              └──── SQLite or Postgres
```

- `frontend/`: SvelteKit 2 and Svelte 5, TypeScript. The browser only talks to SvelteKit.
- `backend/`: FastAPI. Prompts, validation, streaming, history, progress, catalog of modules.
- Ollama runs the language model.

## Requirements

- Python 3.11 or newer
- Node.js 20 or newer
- [Ollama](https://ollama.com/download)
- Chrome or Edge for the microphone (or Whisper, see below)

## Quick start

```bash
# 1. The model (about 2.5 GB, once)
ollama pull qwen3:4b

# 2. Backend
cd backend
python -m venv .venv
.venv\Scripts\activate            # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env              # Windows: copy .env.example .env
uvicorn app.main:app --reload     # API docs: http://127.0.0.1:8000/docs

# 3. Frontend (second terminal)
cd frontend
cp .env.example .env
npm install
npm run dev                       # http://localhost:5173
```

The badge at the bottom of the sidebar shows whether the server, Ollama and the model are ready. The first launch asks for your name, language and level.

**Voice conversation:** open Talk, press the voice conversation button and allow the microphone. Speak, stop talking, and the coach answers. If you stay silent three times in a row it pauses. With Chrome or Edge, the browser's speech recognition sends your audio to the browser vendor's servers; use Whisper (below) to keep everything local.

## Profiles and privacy

Each person picks a first name, and every profile has its own history, progress and word list. There is no password: fine for you and people you trust on the same machine or network. Add real authentication before exposing the app to the internet.

## Database: SQLite or Postgres

SQLite is the default and needs nothing: the file lives in `backend/data/`. Tables are created at startup.

For Postgres without installing it, use Docker:

```bash
docker compose up -d db                     # starts Postgres in a container
pip install -r backend/requirements-postgres.txt
```

Then set `DB_MODE=postgres` in `backend/.env` (the `POSTGRES_*` values already match `docker-compose.yml`) and restart the backend. Set `DB_MODE=sqlite` to go back. Data in each database stays separate. `DATABASE_URL` overrides everything if you need a custom connection.

## Better voice (optional)

Without this step the app uses the browser's microphone and voice. For Whisper (speech to text, local) and Piper (natural English voice):

```bash
cd backend
pip install -r requirements-speech.txt
python -m piper.download_voices en_US-lessac-medium --data-dir models/piper
```

Restart the backend. The settings page shows when the server voice is active. If the download command differs for your Piper version, put `en_US-lessac-medium.onnx` and its `.json` file in `backend/models/piper/`.

## Adding things

Everything the model can do is exposed through three small catalogs in `backend/app/catalog/`. Add one entry and it appears in the app, in both languages, with no frontend change:

| To add | Edit | What to write |
| --- | --- | --- |
| A Studio module (poems, letters, anything text) | `tools.py` | One `Tool(...)`: id, titles, instructions for the model, optional choices |
| A conversation situation | `scenarios.py` | One `Scenario(...)`: label, prompt, first line |
| A conversation topic chip | `topics.py` | One `Topic(...)`: label, first line |

Studio results are saved to your progress automatically. New skills for the progress page go in `backend/app/schemas/common.py` and the two `skill.*` text entries.

## Growing it

- Several people: raise `MAX_CONCURRENT_GENERATIONS` and set `OLLAMA_NUM_PARALLEL` on Ollama if the GPU allows it, or run Ollama on a stronger machine and set `OLLAMA_BASE_URL`.
- The backend keeps no state in memory, so you can run several copies behind a load balancer once you use Postgres.
- Next steps: real accounts, database migrations (Alembic), a learning timeline.

## License

MIT
