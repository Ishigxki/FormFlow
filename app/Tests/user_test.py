from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "welcome to Formflow API"
    }

def test_get_user():
    response = client.get("/users")

    assert response.status_code == 200

    assert response.json() == {

    }

def test_get_user_by_ID():
    response =client.get("/user/{}")

    assert response.status_code == 200
    