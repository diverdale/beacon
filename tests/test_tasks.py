# NOTE: PUT and DELETE endpoints intentionally have no tests.
# This is a training artifact — module 5 has learners add them.
import pytest
from app.models import User, Project, Task


@pytest.fixture
def seed_data(db, app):
    with app.app_context():
        user = User(name="Alice", email="alice@tasks.dev")
        project = Project(name="Core")
        db.session.add_all([user, project])
        db.session.flush()
        task = Task(title="Write docs", status="todo",
                    assignee_id=user.id, project_id=project.id)
        db.session.add(task)
        db.session.commit()
        return {"user_id": user.id, "project_id": project.id, "task_id": task.id}


def test_list_tasks_empty(client, db):
    resp = client.get("/api/tasks")
    assert resp.status_code == 200
    assert resp.json == []


def test_create_task(client, db, seed_data, app):
    with app.app_context():
        data = seed_data
    resp = client.post(
        "/api/tasks",
        json={
            "title": "New task",
            "project_id": data["project_id"],
            "assignee_id": data["user_id"],
        },
    )
    assert resp.status_code == 201
    assert resp.json["title"] == "New task"
    assert resp.json["status"] == "todo"


def test_create_task_missing_title(client, db):
    resp = client.post("/api/tasks", json={"project_id": 1})
    assert resp.status_code == 400
    assert "error" in resp.json


def test_get_task_by_id(client, db, seed_data, app):
    with app.app_context():
        task_id = seed_data["task_id"]
    resp = client.get(f"/api/tasks/{task_id}")
    assert resp.status_code == 200
    assert resp.json["id"] == task_id


def test_get_task_not_found(client, db):
    # BUG: This route raises a 500 instead of returning 404.
    # Intentional — used in module 3 diff-review exercise.
    assert client.get("/api/tasks/9999").status_code in (404, 500)
