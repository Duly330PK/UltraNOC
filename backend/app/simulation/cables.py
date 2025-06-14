
# backend/app/simulation/cables.py
fiber_links = [
    {
        "id": "link-1",
        "from": "core-1",
        "to": "access-1",
        "type": "singlemode",
        "length": 12000,
        "db_loss": 3.2,
        "status": "up"
    },
    {
        "id": "link-2",
        "from": "access-1",
        "to": "ont-1",
        "type": "multimode",
        "length": 800,
        "db_loss": 1.0,
        "status": "up"
    }
]

def list_fiber_links():
    return fiber_links
