import requests

def test_validate_ipv6():
    payload = { "address": "2001:0db8::1" }
    response = requests.post("http://localhost:8000/api/v1/tools/ipv6/analyze", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["valid"] is True