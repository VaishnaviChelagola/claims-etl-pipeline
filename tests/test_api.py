from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_get_claims_summary():
    response = client.get("/claims/summary")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_status_counts():
    response = client.get("/claims/status-counts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    # Check structure
    if len(data) > 0:
        assert "_id" in data[0]
        assert "count" in data[0]


def test_get_claims_by_group():
    response = client.get("/claims/by-group/1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
