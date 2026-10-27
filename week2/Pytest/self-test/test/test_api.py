from fastapi.testclient import TestClient
from main import app,get_repo
from app.repository import TodoRepository
import pytest

@pytest.fixture
def client():
    test_repo = TodoRepository()

    def override_get_repo():
        return test_repo

    app.dependency_overrides[get_repo]= override_get_repo
    yield TestClient(app=app)

    app.dependency_overrides.clear()


def test_create_todo(client):
    json = {
            "title": "string",
            "deadline": "2026-10-27",
            "level": 1
}
    res = client.post("/todos",json=json)
    assert res.status_code == 201
    assert res.json()["id"] == 1

def test_create_duplicate_todo(client):
    json = {
            "title": "string",
            "deadline": "2026-10-27",
            "level": 1
}
    res1 = client.post("/todos",json=json)
    res2 = client.post("/todos",json=json)
    assert res1.status_code ==201
    assert res2.status_code ==409

def test_get_not_found(client):
    res = client.get("/todos/999")
    assert res.status_code == 404

def test_get_invalid_id(client):
    res = client.get("/todos/abc")
    assert res.status_code == 422

def test_update_not_found(client):
    json = {
            "title": "play game",
            "deadline": "2026-10-27",
            "level": 1
}
    res = client.put("todos/999",json=json)
    assert res.status_code == 404

def test_delete_not_found(client):
    res = client.delete("/todos/999")
    assert res.status_code == 404
