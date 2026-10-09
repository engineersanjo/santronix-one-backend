from fastapi.testclient import TestClient

from app.main import app


def test_root_discloses_api_prefix_and_docs() -> None:
    response = TestClient(app).get("/")
    assert response.status_code == 200
    assert response.json()["api"] == "/api/v1"
    assert response.json()["docs"] == "/docs"
