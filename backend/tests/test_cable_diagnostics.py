import requests

BASE_URL = "http://localhost:8000/api/v1/cables/diagnostics"

def test_run_manual_diagnostic():
    data = {
        "cable_id": "fiber123",
        "attenuation_db": 4.7,
        "length_m": 750.0
    }
    response = requests.post(f"{BASE_URL}/run", json=data)
    assert response.status_code == 200
    payload = response.json()
    assert payload["result"] == "PASS"
    assert payload["cable_id"] == "fiber123"

def test_diagnose_auto():
    data = { "cable_id": "fiber456" }
    response = requests.post(f"{BASE_URL}/diagnose", json=data)
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert "loss_db" in payload
