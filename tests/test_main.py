from fastapi.testclient import TestClient

from app.main import app
from app.settings import Settings, get_settings


def get_settings_override():
    return Settings(clerk_secret_key="unit-test-token")


app.dependency_overrides[get_settings] = get_settings_override


def test_root_view_with_config(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert data["clerk_secret_key"] == "unit-test-token"
