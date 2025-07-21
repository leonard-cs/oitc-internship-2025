from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_ping():
    response = client.get("/api/health/ping")
    assert response.status_code == 200
