from __future__ import annotations


def test_health_ping(client):
    response = client.get("/api/health/ping")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
