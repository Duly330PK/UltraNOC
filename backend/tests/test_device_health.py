import requests

def test_report_health():
    data = {
        "device": "RouterX",
        "cpu_usage": 65.4,
        "memory_usage": 72.1
    }
    response = requests.post("http://localhost:8000/api/v1/devices/health/report", json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["device"] == "RouterX"