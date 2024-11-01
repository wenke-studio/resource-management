from fastapi.testclient import TestClient

from .main import app
from .settings import Settings, get_settings

client = TestClient(app)


def get_settings_override():
    return Settings(token="unit-test-token")


app.dependency_overrides[get_settings] = get_settings_override


def test_root_view_with_config():
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert data["token"] == "unit-test-token"
