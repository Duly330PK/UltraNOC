# C:\noc_project\UltraNOC\backend\tests\test_metrics.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_all_metrics():
    response = client.get("/api/v1/metrics/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    if response.json():
        metric = response.json()[0]
        assert "device_id" in metric
        assert "metric_type" in metric
        assert "value" in metric
        assert "timestamp" in metric
