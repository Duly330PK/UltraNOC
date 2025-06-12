from typing import List, Dict
from datetime import datetime
import uuid

active_alarms: Dict[str, dict] = {}

def trigger_alarm(device_id: str, alarm_type: str, severity: str, message: str) -> dict:
    alarm_id = str(uuid.uuid4())
    alarm = {
        "id": alarm_id,
        "device_id": device_id,
        "type": alarm_type,
        "severity": severity,
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
        "acknowledged": False
    }
    active_alarms[alarm_id] = alarm
    return alarm

def get_active_alarms() -> List[dict]:
    return list(active_alarms.values())

def clear_alarm(alarm_id: str) -> bool:
    if alarm_id in active_alarms:
        del active_alarms[alarm_id]
        return True
    return False

def monitor_interface_status(device_id: str, interface: str, status: str):
    if status.lower() == "down":
        return trigger_alarm(device_id, "interface_down", "critical", f"{interface} is down")
    return None

def monitor_traffic_threshold(device_id: str, rx_mbps: float, tx_mbps: float, threshold: float = 900.0):
    if rx_mbps > threshold or tx_mbps > threshold:
        return trigger_alarm(
            device_id, "traffic_overload", "major",
            f"High traffic detected: RX={rx_mbps}Mbps, TX={tx_mbps}Mbps"
        )
    return None
