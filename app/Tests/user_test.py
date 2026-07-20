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

    assert isinstance(response.json(), list)

def test_get_user_by_id():

    response = client.get("/users/2")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 2

def test_user_not_found():

    response = client.get("/users/999")

    assert response.status_code == 404
    