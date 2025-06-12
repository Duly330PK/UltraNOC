from typing import Dict, List

# VLAN-Struktur pro Gerät
vlan_db: Dict[str, dict] = {}

def create_vlan(device_id: str, vlan_id: int, name: str = ""):
    device_vlans = vlan_db.setdefault(device_id, {"vlans": {}, "trunks": {}})
    device_vlans["vlans"][str(vlan_id)] = {
        "name": name,
        "ports": []
    }

def assign_port_to_vlan(device_id: str, port: str, vlan_id: int):
    device_vlans = vlan_db.setdefault(device_id, {"vlans": {}, "trunks": {}})
    vlan = device_vlans["vlans"].setdefault(str(vlan_id), {"name": "", "ports": []})
    if port not in vlan["ports"]:
        vlan["ports"].append(port)

def configure_trunk_port(device_id: str, port: str, allowed_vlans: List[int]):
    device_vlans = vlan_db.setdefault(device_id, {"vlans": {}, "trunks": {}})
    device_vlans["trunks"][port] = allowed_vlans

def get_vlan_table(device_id: str) -> dict:
    return vlan_db.get(device_id, {"vlans": {}, "trunks": {}})

def is_vlan_allowed(device_id: str, port: str, vlan_id: int) -> bool:
    trunk = vlan_db.get(device_id, {}).get("trunks", {}).get(port, [])
    return vlan_id in trunk
