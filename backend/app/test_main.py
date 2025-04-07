import pytest
from fastapi.testclient import TestClient
from .main import app
from .database import DB
from typing import List

client = TestClient(app)


@pytest.fixture
def auth_token():
    response = client.post(f"/token?username=johndoe&password=secret")
    token_data = response.json()
    return token_data["access_token"]


def test_up():
    response = client.get("/up")
    assert response.status_code == 200


def test_login_success():
    response = client.post(f"/token?username=johndoe&password=secret")
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"


def test_read_users_me(auth_token):
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {auth_token}"}
    )
    user = response.json()

    assert response.status_code == 200
    assert user["username"] == "johndoe"
    assert user["full_name"] == "John Doe"
    assert user["email"] == "johndoe@example.com"


def test_read_fruits(auth_token):
    response = client.get("/fruits", headers={"Authorization": f"Bearer {auth_token}"})
    fruits = response.json()

    assert response.status_code == 200
    assert isinstance(fruits, List)


def test_read_fruits_without_auth():
    response = client.get("/fruits")
    assert response.status_code == 401


def test_create_fruits(auth_token):
    response = client.post(
        "/fruits",
        json={"name": "orange"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    new_fruit = response.json()

    assert response.status_code == 200
    assert new_fruit["name"] == "orange"
    assert DB.fruits[new_fruit["id"]].name == "orange"


def test_create_fruits_without_auth():
    response = client.post("/fruits", json={"name": "orange"})
    assert response.status_code == 401


def test_update_fruit(auth_token):
    response = client.put(
        "/fruits/1",
        json={"name": "kiwi"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    updated_fruit = response.json()

    assert response.status_code == 200
    assert updated_fruit["name"] == "kiwi"
    assert DB.fruits[1].name == "kiwi"


def test_update_fruit_without_auth():
    response = client.put("/fruits/1", json={"name": "kiwi"})
    assert response.status_code == 401


def test_delete_fruit(auth_token):
    response = client.delete(
        "/fruits/1", headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert 1 not in DB.fruits


def test_delete_fruit_without_auth():
    response = client.delete("/fruits/1")
    assert response.status_code == 401
