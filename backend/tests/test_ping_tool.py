import requests

def test_ping_simulation():
    data = { "target": "192.0.2.1" }
    response = requests.post("http://localhost:8000/api/v1/tools/ping", json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["target"] == "192.0.2.1"
    assert result["status"] in ["reachable", "unreachable", "error"]
    assert "output" in result or "message" in result or "error" in result
