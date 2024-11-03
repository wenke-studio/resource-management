from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.authentication.dependencies import get_user
from app.databases import get_session
from app.main import app
from app.user.models import User

TEST_USER = {
    "id": "9999",
    "username": "test-user",
    "email": "test-user@email.com",
}


@pytest.fixture(scope="session")
def db_engine():
    sqlite_file_name = "test-database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, connect_args=connect_args, echo=True)
    SQLModel.metadata.create_all(engine)
    # add the test user to the database
    with Session(engine) as session:
        session.add(User(**TEST_USER))
        session.commit()
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator[Session, None, None]:
    # create a new session for each test
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function", name="test_user")
def get_test_user(db_session: Session):
    yield db_session.get(User, TEST_USER["id"])


@pytest.fixture(scope="function")
def client(db_session) -> Generator[TestClient, None, None]:
    def override_get_session():
        yield db_session

    def override_get_user():
        # override the current logged in user to be test_user
        yield db_session.get(User, TEST_USER["id"])

    # override dependencies
    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_user] = override_get_user
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
