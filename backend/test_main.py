from fastapi.testclient import TestClient
from .main import app, fruits_db
from typing import List

client = TestClient(app)


def test_read_fruits():
    response = client.get("/fruits", headers={})
    fruits = response.json()

    assert response.status_code == 200
    assert isinstance(fruits, List)


def test_read_fruit():
    response = client.get("/fruits/1")
    fruit = response.json()

    assert response.status_code == 200
    assert fruit["id"] == 1


def test_create_fruits():
    response = client.post("/fruits", json={"name": "orange"})
    new_fruit = response.json()

    assert response.status_code == 200
    assert new_fruit["name"] == "orange"
    assert fruits_db[new_fruit["id"]].name == "orange"


def test_update_fruit():
    response = client.put("/fruits/1", json={"name": "kiwi"})
    updated_fruit = response.json()

    assert response.status_code == 200
    assert updated_fruit["name"] == "kiwi"
    assert fruits_db[1].name == "kiwi"


def test_delete_fruit():
    response = client.delete("/fruits/1")
    assert response.status_code == 200
    assert 1 not in fruits_db
