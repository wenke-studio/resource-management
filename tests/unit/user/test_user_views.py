from faker import Faker
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.user.models import User

fake = Faker()


def test_create_user(client: TestClient, db_session: Session):
    # create a user
    payload = {
        "id": fake.uuid4(),
        "email": fake.email(),
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 200

    # check if the user is created
    user = db_session.get(User, payload["id"])
    assert user is not None
    assert user.email == payload["email"]


def test_read_users(client: TestClient):
    # create a user
    payload = {
        "id": fake.uuid4(),
        "username": fake.user_name(),
        "email": fake.email(),
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 200

    # list all users
    response = client.get("/users/")
    assert response.status_code == 200

    # assert the user is in the list
    body = response.json()
    assert payload in body


def test_retrieve_user(client: TestClient):
    payload = {
        "id": fake.uuid4(),
        "email": fake.email(),
        "username": fake.user_name(),
    }

    # try to retrieve a user that does not exist
    response = client.get(f"/users/{payload['id']}")
    assert response.status_code == 404

    # create a user
    response = client.post("/users/", json=payload)
    assert response.status_code == 200

    # get the user
    response = client.get(f"/users/{payload['id']}")
    assert response.status_code == 200

    # assert the user is correct
    body = response.json()
    assert payload == body


def test_delete_user(client: TestClient, db_session: Session):
    # create a user
    payload = {
        "id": fake.uuid4(),
        "email": fake.email(),
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 200

    # delete the user
    response = client.delete(f"/users/{payload['id']}")
    assert response.status_code == 200

    # check if the user is deleted
    user = db_session.get(User, payload["id"])
    assert user is None
