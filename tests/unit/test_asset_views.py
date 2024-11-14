from faker import Faker
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from sqlmodel import Session, select

from app.asset.models import Asset

fake = Faker()


def test_create_asset(client: TestClient, db_session: Session, mocker: MockerFixture):
    mocker.patch("app.asset.views.file_storage")

    upload_file = (fake.file_name(), fake.image(image_format="tiff"))
    response = client.post("/assets/", files={"upload_file": upload_file})
    assert response.status_code == 201, response.status_code

    asset = response.json()
    record = db_session.exec(select(Asset).where(Asset.id == asset["id"])).first()
    assert asset == record.model_dump()


def test_list_assets(client: TestClient, db_session: Session, mocker: MockerFixture):
    mocker.patch("app.asset.views.file_storage")

    response = client.post(
        "/assets/",
        files={"upload_file": (fake.file_name(), fake.image())},
    )
    assert response.status_code == 201

    response = client.get("/assets/")
    assert response.status_code == 200
    assets = db_session.exec(select(Asset)).all()
    assert response.json() == [asset.model_dump() for asset in assets]


def test_retrieve_asset_view(client: TestClient, mocker: MockerFixture):
    mocker.patch("app.asset.views.file_storage")

    response = client.post(
        "/assets/",
        files={"upload_file": (fake.file_name(), fake.image())},
    )
    assert response.status_code == 201
    asset = response.json()

    response = client.get(f"/assets/{asset['id']}")
    assert response.status_code == 200
    assert response.json() == asset


def test_delete_asset_view(
    client: TestClient, db_session: Session, mocker: MockerFixture
):
    mocker.patch("app.asset.views.file_storage")

    response = client.post(
        "/assets/",
        files={"upload_file": (fake.file_name(), fake.image())},
    )
    assert response.status_code == 201
    asset = response.json()

    response = client.delete(f"/assets/{asset['id']}")
    assert response.status_code == 204

    record = db_session.get(Asset, asset["id"])
    assert record is None
