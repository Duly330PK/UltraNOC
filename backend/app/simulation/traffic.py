import random
import datetime
from typing import Dict, List

# Simulierte Datenbank für Traffic Sessions (in Memory)
TRAFFIC_SESSIONS = []

def simulate_traffic_flow(src_device: str, dst_device: str, bandwidth_mbps: float, duration_s: int):
    """Erzeugt eine simulierte Verkehrssitzung zwischen zwei Geräten"""
    session = {
        "id": f"{src_device}-{dst_device}-{datetime.datetime.now().timestamp()}",
        "source": src_device,
        "destination": dst_device,
        "bandwidth_mbps": bandwidth_mbps,
        "duration_s": duration_s,
        "start_time": datetime.datetime.now().isoformat(),
        "qos_tag": apply_qos_policies(src_device, dst_device, bandwidth_mbps)
    }
    TRAFFIC_SESSIONS.append(session)
    log_flow_session(session)
    return session

def calculate_bandwidth_burst(base_bw: float) -> float:
    """Erzeugt einen kurzen Traffic Burst über dem Durchschnitt"""
    return round(base_bw * random.uniform(1.1, 1.8), 2)

def apply_qos_policies(src: str, dst: str, bw: float) -> str:
    """Simuliert einfache QoS-Priorisierung anhand von Schwellen"""
    if bw > 500:
        return "bulk"
    elif "core" in src or "edge" in dst:
        return "realtime"
    return "best-effort"

def log_flow_session(session: Dict):
    print(f"[TRAFFIC] {session['source']} → {session['destination']} | {session['bandwidth_mbps']} Mbps | {session['qos_tag']}")

def get_all_sessions() -> List[Dict]:
    return TRAFFIC_SESSIONS
