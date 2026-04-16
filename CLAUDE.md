# Beacon — AI Context

## What is this?
Beacon is a task management REST API for an internal engineering team.

## Stack
- Python 3.11+ / Flask 3.x
- SQLAlchemy 2.x with SQLite (dev)
- pytest for testing

## Project structure
- `app/` — Flask application
  - `models.py` — SQLAlchemy models: User, Project, Task
  - `routes/` — Flask blueprints, one per resource
  - `services/` — Business logic layer (called by routes)
  - `database.py` — SQLAlchemy setup
- `tests/` — pytest tests
- `run.py` — development entrypoint

## Running locally
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

## Running tests
```bash
pytest tests/ -v
```

## API base URL
All routes are prefixed with `/api/`. Resources: `/api/users`, `/api/projects`, `/api/tasks`.

## Conventions
- Routes return JSON. Errors always include an `"error"` key.
- Task statuses: `todo`, `in_progress`, `done`, `archived`
- Use `to_dict()` on models to serialize for responses.
