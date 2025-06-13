import requests

def test_raise_incident():
    url = "http://localhost:8000/api/v1/incidents/raise?source=Node5&impact=link_failure"
    response = requests.post(url)
    assert response.status_code == 200
    result = response.json()
    assert result["impact"] == "link_failure"