import pytest
from app.models import User


@pytest.fixture
def seed_users(db, app):
    with app.app_context():
        u1 = User(name="Alice", email="alice@beacon.dev")
        u2 = User(name="Bob", email="bob@beacon.dev")
        db.session.add_all([u1, u2])
        db.session.commit()
        return [u1.id, u2.id]


def test_get_users_empty(client, db):
    resp = client.get("/api/users")
    assert resp.status_code == 200
    assert resp.json == []


def test_create_user(client, db):
    resp = client.post(
        "/api/users",
        json={"name": "Carol", "email": "carol@beacon.dev"},
    )
    assert resp.status_code == 201
    data = resp.json
    assert data["name"] == "Carol"
    assert data["email"] == "carol@beacon.dev"
    assert "id" in data


def test_create_user_missing_email(client, db):
    resp = client.post("/api/users", json={"name": "Dana"})
    assert resp.status_code == 400
    assert "error" in resp.json


def test_create_user_duplicate_email(client, db):
    client.post("/api/users", json={"name": "Eve", "email": "eve@beacon.dev"})
    resp = client.post("/api/users", json={"name": "Eve2", "email": "eve@beacon.dev"})
    assert resp.status_code == 409
    assert "error" in resp.json


def test_get_user_by_id(client, db, seed_users, app):
    with app.app_context():
        user_id = seed_users[0]
    resp = client.get(f"/api/users/{user_id}")
    assert resp.status_code == 200
    assert resp.json["id"] == user_id


def test_get_user_not_found(client, db):
    resp = client.get("/api/users/9999")
    assert resp.status_code == 404
    assert "error" in resp.json


def test_delete_user(client, db, seed_users, app):
    with app.app_context():
        user_id = seed_users[0]
    resp = client.delete(f"/api/users/{user_id}")
    assert resp.status_code == 204
    resp2 = client.get(f"/api/users/{user_id}")
    assert resp2.status_code == 404
