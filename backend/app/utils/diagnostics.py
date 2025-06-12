from random import choice

def test_interface_health(interface_name: str) -> str:
    return choice(["OK", "Degraded", "Down"])

def loopback_test(device_id: str) -> str:
    return f"Loopback test initiated on {device_id}... OK"

def simulate_latency_test(src: str, dst: str) -> float:
    import random
    return round(random.uniform(1.0, 15.0), 2)
