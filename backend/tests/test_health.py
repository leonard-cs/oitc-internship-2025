from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health_ping():
    response = client.get("api/v1/health/ping")
    assert response.status_code == 200
