import requests

def test_add_task():
    task = {
        "task": "Backup DB",
        "run_at": "2025-06-14T02:00:00"
    }
    response = requests.post("http://localhost:8000/api/v1/scheduler/add", json=task)
    assert response.status_code == 200
    result = response.json()
    assert result["task"] == "Backup DB"