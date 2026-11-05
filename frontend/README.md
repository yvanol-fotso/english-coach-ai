# Frontend

SvelteKit 2 and Svelte 5 (runes), TypeScript, adapter-node.

## Run

```bash
cp .env.example .env
npm install
npm run dev          # http://localhost:5173
npm run check        # type-check
npm run build && npm start
```

`BACKEND_URL` (default `http://127.0.0.1:8000/api/v1`) is read on the server only.

## Data flow

```
+page.svelte ── lib/services/api.ts ── /api/<name> ── routes/api/<name>/+server.ts ── lib/server/backend.ts ── FastAPI
+page.server.ts ── backendGet() ───────────────────────────────────────────────────────────────────────────── FastAPI
```

The browser never calls FastAPI directly. Proxies forward the method, query and body, and add the `X-Profile` header from the `ec_profile` cookie. Pages that only read data (history, progress, vocabulary, home) load it in `+page.server.ts`, so they render with their data already in place.

## Routes

| Route | Purpose | Components |
| --- | --- | --- |
| `/` | Home, setup help, streak | |
| `/path`, `/path/[unit]` | Beginner course: discover, repeat, dialogue, quiz | `components/path/` |
| `/chat` | Free conversation, voice mode, history rail (`/chat?c=ID` reopens one) | `components/chat/` |
| `/call` | Phone-style voice call and review | `components/call/` |
| `/ask` | Short spoken or written answers to language questions | `components/ask/` |
| `/drills` | Pronunciation and dictation with word-by-word score | `components/practice/` |
| `/studio`, `/studio/[id]` | Studio tools, built from the backend catalog | `components/ui/` |
| `/correct` | Writing corrections | `components/correct/` |
| `/practice` | Reading and listening quizzes | `components/practice/` |
| `/translate` | FR/EN translation | `components/translate/` |
| `/vocabulary`, `/vocabulary/review` | Explanations, saved words, spaced-repetition review | `components/vocabulary/` |
| `/history` | Saved conversations | `components/history/` |
| `/progress` | Streak, skills, activity | `components/progress/` |
| `/settings` | Profile, language, theme, level, voice | `components/settings/` and `components/ui/` |
| `/api/*` | Proxies (chat, tools, drills, translate, correct, practice, explain, speech, activities, words, conversations, health) | |

## Structure

```
src/
  hooks.server.ts       reads preferences cookies, sets html lang/theme/accent, security headers
  hooks.client.ts
  routes/
    +layout.server.ts   health, preferences, profile
    +layout.svelte      shell, welcome dialog
    +error.svelte
    api/<name>/+server.ts
    <route>/+page.svelte, +page.server.ts
  lib/
    actions/            autoresize, autoscroll
    components/<route>/ one folder per route, plus layout/ and ui/
    data/               levels
    i18n/               fr.ts, en.ts, index.svelte.ts (t, plural)
    server/             backend.ts (forward, backendGet, getHealth), prefs.ts
    services/           api.ts (typed client), speech.ts (voice out, dictation with silence detection)
    stores/             preferences (language, theme, accent), settings (level, voice, corrections)
    types/              shared types
```

## Catalog-driven screens

Topics, situations and Studio tools come from `GET /catalog` (loaded in `+layout.server.ts`). Their labels are bilingual objects `{ fr, en }`, shown with `pick()`. To add one, edit `backend/app/catalog/`; no frontend change is needed.

## Voice

`lib/services/voiceLoop.svelte.ts` runs the hands-free loop used by Talk and Call: listen (auto-stop on silence) → send → correction and reply stream in → speak → listen again. `lib/services/conversation.svelte.ts` holds the shared conversation state and streaming. Speech output and dictation live in `lib/services/speech.ts`.

## Languages

The language being learned is the `ec_target` cookie (`preferences.target`), so server loaders can use it. `lib/data/languages.ts` maps language codes to speech locales.

## Translations

All text lives in `lib/i18n/fr.ts` and `en.ts`. The English file is type-checked against the French one, so a missing key fails `npm run check`. Use `t('key', { name })` in components. Language, theme and accent are stored in cookies so the server renders the right version from the first byte.

## Brand and metadata

`static/` has the favicon (a smiling speech bubble), app icons, `og.png`, `site.webmanifest` and `robots.txt`. `src/app.html` holds the meta tags; `hooks.server.ts` fills the description by language and the absolute `og:image` URL. In production set `ORIGIN`.

## Design

Tokens (colors, radius, fonts) are in `src/app.css`. Light and dark are set with `data-theme` on `<html>`, accent colors with `data-accent`. Fonts (Bricolage Grotesque, Figtree) come from `@fontsource`, so the app works offline.

## Speech

`lib/services/speech.ts` uses the backend (Whisper recording, Piper playback) when `/health` reports `stt` or `tts`, and falls back to the browser's Web Speech API otherwise.
