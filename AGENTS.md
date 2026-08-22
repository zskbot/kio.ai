# Base44 Dev Environment

## What this is
KIO.ai — a self-contained Python (aiohttp) web app. `server.py` serves `index.html` + static assets and a REST/WS API on port 8080. `agent_router.py` is a pure-Python keyword router (no external calls) that selects skills/tools/files and builds a plan for a task.

## Run
```
docker compose -f docker-compose.base44.yml up -d
```
- Web entry point: host port **3000** → container 8080.
- Image: `python:3.12-slim`; deps (`aiohttp`, `watchfiles`) installed at startup.
- Source is bind-mounted at `/app`; `watchfiles` restarts `python server.py` on file changes (live reload).

## Secrets
All API keys are **optional** — the app boots and the core agent router works without any. They only power the optional plugin integrations (OpenAI, Anthropic, Google AI, GitHub, Vercel), which report `NOT_CONFIGURED` when absent. Delivered via `/run/base44/app.env` (compose `env_file`). `server.py` also reads a repo `.env` via `os.environ.setdefault`, but the platform env file takes precedence.

## Verify
- `curl -sf http://localhost:3000/` → returns `index.html`.
- `curl -sf http://localhost:3000/api/tools` → JSON tool list.
- aiohttp binds `0.0.0.0` and does not gate by Host, so the external preview hostname works without extra config.
