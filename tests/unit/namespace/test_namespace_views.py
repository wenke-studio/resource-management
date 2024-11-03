from faker import Faker
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.namespace.models import Namespace

fake = Faker()


def test_create_namespace(client: TestClient, db_session: Session):
    # create a namespace
    payload = {
        "id": fake.uuid4(),
        "name": fake.company(),
    }
    response = client.post("/namespaces/", json=payload)
    assert response.status_code == 200

    # check if the namespace is in the database
    namespace = db_session.get(Namespace, payload["id"])
    assert namespace is not None
    assert namespace.name == payload["name"]
