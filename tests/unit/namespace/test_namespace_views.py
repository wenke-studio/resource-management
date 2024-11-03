from faker import Faker
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.namespace.models import Namespace
from app.user.models import User

fake = Faker()


def test_create_namespace(client: TestClient, db_session: Session, test_user: User):
    # create a namespace
    payload = {
        "id": fake.uuid4(),
        "name": fake.company(),
    }
    response = client.post("/namespaces/", json=payload)
    assert response.status_code == 200
    assert payload == response.json()

    # check if the namespace is in the database
    namespace = db_session.get(Namespace, payload["id"])
    assert namespace is not None
    assert namespace.id == payload["id"]
    assert namespace.name == payload["name"]
    assert test_user in namespace.members


def test_read_namespaces(client: TestClient):
    # create a namespace
    payload = {
        "id": fake.uuid4(),
        "name": fake.company(),
    }
    response = client.post("/namespaces/", json=payload)
    assert response.status_code == 200

    # list all namespaces
    response = client.get("/namespaces/")
    assert response.status_code == 200
    # assert the namespace is in the list
    assert payload in response.json()


def test_retrieve_namespace(client: TestClient):
    # create a namespace
    payload = {
        "id": fake.uuid4(),
        "name": fake.company(),
    }
    response = client.post("/namespaces/", json=payload)
    assert response.status_code == 200

    # retrieve the namespace
    response = client.get(f"/namespaces/{payload['id']}")
    assert response.status_code == 200
    assert payload == response.json()


def test_delete_namespace(client: TestClient, db_session: Session, test_user: User):
    # create a namespace
    payload = {
        "id": fake.uuid4(),
        "name": fake.company(),
    }
    response = client.post("/namespaces/", json=payload)
    assert response.status_code == 200

    # delete the namespace
    response = client.delete(f"/namespaces/{payload['id']}")
    assert response.status_code == 200
