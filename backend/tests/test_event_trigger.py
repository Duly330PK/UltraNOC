import requests

def test_event_trigger():
    event = {
        "source": "UPS1",
        "event_type": "battery",
        "detail": "Voltage drop detected"
    }
    response = requests.post("http://localhost:8000/api/v1/events/trigger", json=event)
    assert response.status_code == 200
    payload = response.json()
    assert payload["event_type"] == "battery"