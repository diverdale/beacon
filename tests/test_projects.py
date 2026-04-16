# NOTE: Only happy-path tests — intentional for training purposes.
# Missing: 404 handling, duplicate names, invalid input.
import pytest
from app.models import Project


def test_create_project(client, db):
    resp = client.post(
        "/api/projects",
        json={"name": "Backend", "description": "Core API work"},
    )
    assert resp.status_code == 201
    assert resp.json["name"] == "Backend"


def test_list_projects(client, db):
    client.post("/api/projects", json={"name": "Alpha"})
    client.post("/api/projects", json={"name": "Beta"})
    resp = client.get("/api/projects")
    assert resp.status_code == 200
    assert len(resp.json) == 2
