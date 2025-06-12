from typing import Dict
import math

fiber_links: Dict[str, dict] = {}

def register_fiber_link(link_id: str, from_device: str, to_device: str, length_km: float, fiber_type: str = "SMF", core_count: int = 2):
    # dB Verlust pro km (z. B. SMF = 0.2dB/km)
    loss_per_km = {
        "SMF": 0.2,
        "MMF": 0.5,
        "UDF": 0.1
    }.get(fiber_type.upper(), 0.25)

    fiber_links[link_id] = {
        "from": from_device,
        "to": to_device,
        "length_km": length_km,
        "fiber_type": fiber_type,
        "core_count": core_count,
        "db_loss": round(length_km * loss_per_km, 3),
        "latency_ms": round(length_km * 0.005, 3),
        "status": "active"
    }

def get_link(link_id: str) -> dict:
    return fiber_links.get(link_id, {})

def simulate_link_failure(link_id: str):
    if link_id in fiber_links:
        fiber_links[link_id]["status"] = "down"

def restore_link(link_id: str):
    if link_id in fiber_links:
        fiber_links[link_id]["status"] = "active"

def list_fiber_links() -> Dict[str, dict]:
    return fiber_links
