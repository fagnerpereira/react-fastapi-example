from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_get_fruits():
    response = client.get("/fruits", headers={})
    assert response.status_code == 200
    assert response.json() == {
        "fruits": [{"name": "apple"}, {"name": "banana"}, {"name": "orange"}]
    }
