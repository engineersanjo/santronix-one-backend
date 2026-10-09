from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint_reports_live_process() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "SANTRONIX ONE Backend"
    assert response.headers["X-Request-ID"] == body["request_id"]


def test_readiness_does_not_claim_unconfigured_dependencies() -> None:
    response = client.get("/api/v1/ready")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ready"
    assert body["dependencies"]["database"] == "not_configured"
    assert body["dependencies"]["message_broker"] == "not_configured"
    assert body["dependencies"]["authentication"] == "not_configured"


def test_request_id_is_generated_when_header_is_invalid() -> None:
    response = client.get("/api/v1/health", headers={"X-Request-ID": "x" * 101})
    assert response.status_code == 200
    assert len(response.headers["X-Request-ID"]) == 36


def test_unknown_route_returns_consistent_error_shape() -> None:
    response = client.get("/api/v1/not-a-route")
    assert response.status_code == 404
    body = response.json()
    assert body["code"] == "HTTP_404"
    assert body["status"] == 404
    assert body["instance"] == "/api/v1/not-a-route"
    assert body["request_id"] == response.headers["X-Request-ID"]
