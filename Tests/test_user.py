from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {"message":"Welcome to formflow API"}

def test_get_user():


    response = client.get("/users")

    assert response.status_code == 200

    assert isinstance(response.json(), list)

def test_create_and_get_user():

    # Create a user
    create_response = client.post(
        "/users",
        json={
            "username": "Rick",
            "email": "rick@test.com",
            "password": "password123"
        }
    )

    assert create_response.status_code == 200

    created_user = create_response.json()

    # Retrieve the same user
    get_response = client.get(f"/users/{created_user['id']}")

    assert get_response.status_code == 200

    data = get_response.json()

    assert data["username"] == "Rick"
    assert data["email"] == "rick@test.com"

def test_user_not_found():

    response = client.get("/users/999")

    assert response.status_code == 404
    