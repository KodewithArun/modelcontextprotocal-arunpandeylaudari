# Expences Tracker — MCP + FastAPI

A personal finance tracker that works two ways:

- **MCP Server** — AI assistants (opencode, Claude) manage expenses via natural language
- **FastAPI** — REST API for programmatic access

## Architecture

```
┌──────────────────────┐
│    AI Assistant      │
│  (opencode / Claude) │
└────────┬─────────────┘
         │ MCP (stdio)
         ▼
┌─────────────────────────────────────┐
│  main.py — FastMCP.from_fastapi()  │
│  │                                  │
│  │ httpx calls to localhost:8765    │
│  ▼                                  │
│  app.py — FastAPI (port 8765)       │
│  │                                  │
│  ▼                                  │
│  db.py — SQLite (expenses.db)       │
└─────────────────────────────────────┘
```

## Structure

| File | Purpose |
|------|---------|
| `db.py` | Shared DB layer (SQLite connection + init) |
| `app.py` | FastAPI app with JSON API endpoints |
| `main.py` | FastMCP wrapper (from_fastapi) + auto-starts FastAPI |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/categories` | List categories |
| POST | `/api/categories` | Create category |
| DELETE | `/api/categories/{id}` | Delete category |
| GET | `/api/transactions` | List transactions |
| POST | `/api/transactions` | Add transaction |
| DELETE | `/api/transactions/{id}` | Delete transaction |
| GET | `/api/summary` | Monthly summary |

## Quick Start

```bash
uv sync
python main.py          # runs MCP server (stdio)
uvicorn app:app --port 8000   # or run API standalone
```
