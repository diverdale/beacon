# Beacon

Internal task management API for the Beacon engineering team.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

## Running tests

```bash
pytest tests/ -v
```

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/users | List all users |
| POST | /api/users | Create a user |
| GET | /api/users/:id | Get a user |
| DELETE | /api/users/:id | Delete a user |
| GET | /api/projects | List all projects |
| POST | /api/projects | Create a project |
| GET | /api/tasks | List tasks (optional: ?project_id=) |
| POST | /api/tasks | Create a task |
| GET | /api/tasks/:id | Get a task |
| PUT | /api/tasks/:id | Update a task |
| DELETE | /api/tasks/:id | Delete a task |
| PATCH | /api/tasks/:id/status | Update task status |
