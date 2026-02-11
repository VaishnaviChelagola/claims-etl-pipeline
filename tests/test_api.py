import mongomock
from fastapi.testclient import TestClient
import api

# Create fake MongoDB
mock_client = mongomock.MongoClient()
mock_db = mock_client["claims_reporting"]

# Insert test data
mock_db.claims_summary.insert_many(
    [
        {"claim_id": 1, "status": "Paid"},
        {"claim_id": 2, "status": "Processed"},
    ]
)

mock_db.group_claims_aggregate.insert_one({"group_id": 1, "total_claims": 5})


# Override database dependency
def mock_get_database():
    return mock_db


api.get_database = mock_get_database

client = TestClient(api.app)


def test_get_claims_summary():
    response = client.get("/claims/summary")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_status_counts():
    response = client.get("/claims/status-counts")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_get_claims_by_group():
    response = client.get("/claims/by-group/1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
