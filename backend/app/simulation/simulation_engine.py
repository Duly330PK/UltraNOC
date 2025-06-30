# backend/app/simulation/simulation_engine.py

import json
import asyncio
import random
import aiofiles
import networkx as nx
import uuid
from datetime import datetime, timezone
from app.simulation.connection_manager import ConnectionManager
from app.simulation.threat_correlator import ThreatCorrelator
from app.simulation.plugin_manager import PluginManager
from app.llm_gateway import generate_incident_summary
from app.database import SessionLocal
from app.models.cgnat_log import CGNATLog

ATTACK_PATTERNS = {
    "brute_force_ssh": {
        "sequence": [
            "Brute-force SSH login attempt",
            "Multiple failed logins",
            "Firewall block",
            "Account locked"
        ]
    }
}

class SimulationEngine:
    def __init__(self):
        self.plugin_manager = PluginManager()
        self.topology_data = self._load_json("app/data/live_network_topology.json")
        self.simulation_state = self._load_json("app/data/state.json", default={
            "device_status": {}, "link_status": {}, "device_metrics": {}, "metrics_history": {}
        })
        self.manager = ConnectionManager()
        self.background_tasks = set()
        self.threat_correlator = ThreatCorrelator()
        self.security_simulation_enabled = True
        self.node_map = {
            node['properties']['id']: node
            for node in self.topology_data.get('features', [])
            if node.get('geometry', {}).get('type') == 'Point'
        }
        self.graph = nx.DiGraph() # Use a directed graph for cascading failures
        self._build_network_graph()
        self._apply_initial_state()

    def _load_json(self, file_path, default=None):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"WARNUNG: {file_path} nicht gefunden oder fehlerhaft. Nutze Standardwerte.")
            return default if default is not None else {}

    def get_node_by_id(self, node_id):
        return self.node_map.get(node_id)

    def get_full_topology(self):
        for feature in self.topology_data.get('features', []):
            props = feature['properties']
            if 'id' in props:
                props['status'] = self.simulation_state.get('device_status', {}).get(
                    props['id'], props.get('status', 'unknown'))
        return self.topology_data

    def _build_network_graph(self):
        for feature in self.topology_data.get('features', []):
            if feature.get('geometry', {}).get('type') == 'Point':
                self.graph.add_node(feature['properties']['id'])
        for feature in self.topology_data.get('features', []):
            if feature.get('geometry', {}).get('type') == 'LineString':
                props = feature['properties']
                source, target = props['source'], props['target']
                if self.graph.has_node(source) and self.graph.has_node(target):
                    # Create directed edges from core towards customer
                    self.graph.add_edge(source, target, weight=props.get('details', {}).get('length_km', 1))


    def _apply_initial_state(self):
        for feature in self.topology_data.get('features', []):
            props = feature['properties']
            if 'id' in props and props['id'] in self.simulation_state.get('device_status', {}):
                props['status'] = self.simulation_state['device_status'][props['id']]
            if props.get('source'):
                link_id = f"{props['source']}-{props['target']}"
                if link_id in self.simulation_state.get('link_status', {}):
                    props['status'] = self.simulation_state['link_status'][link_id]

    async def save_state(self):
        async with aiofiles.open("app/data/state.json", "w", encoding="utf-8") as f:
            await f.write(json.dumps(self.simulation_state, indent=2))
        print("Simulationszustand erfolgreich gespeichert.")

    async def run_simulation_loop(self):
        while True:
            await asyncio.gather(
                self._simulate_live_metrics(),
                self._simulate_cgnat_logging(),
                self._simulate_security_incidents()
            )
            await asyncio.sleep(5)

    async def _broadcast_update(self, event_type: str, data: dict):
        await self.manager.broadcast({"type": event_type, "payload": data})

    async def _simulate_live_metrics(self):
        metrics_update = {}
        for node_id, node_data in self.node_map.items():
            props = node_data['properties']
            if props.get('status') == 'online' and not props.get('is_passive', False):
                base_cpu = 15 if "Core" in props.get('type', '') else 5
                cpu = round(random.uniform(base_cpu, base_cpu + 30), 1)
                temp = round(random.uniform(40, 60), 1)
                metrics = {"cpu": cpu, "temp": temp, "timestamp": datetime.now(timezone.utc).isoformat()}

                self.simulation_state['device_metrics'][node_id] = metrics
                history = self.simulation_state['metrics_history'].setdefault(node_id, [])
                history.append(metrics)
                self.simulation_state['metrics_history'][node_id] = history[-60:]
                metrics_update[node_id] = {"current": metrics, "history": history[-60:]}

        if metrics_update:
            await self._broadcast_update("metrics_update", metrics_update)

    async def _simulate_cgnat_logging(self):
        db = SessionLocal()
        try:
            log = CGNATLog(
                customer_id=f"DGF-SIM-{random.randint(1000, 9999)}",
                internal_ip=f"100.75.{random.randint(1,254)}.{random.randint(1,254)}",
                internal_port=random.randint(10000, 65000),
                external_ip="91.194.84.73",
                external_port=random.randint(10000, 65000),
                protocol=random.choice(["TCP", "UDP"]),
                segment=str(random.randint(1, 5))
            )
            db.add(log)
            db.commit()
        finally:
            db.close()

    async def _simulate_security_incidents(self):
        if not self.security_simulation_enabled:
            return
        if random.random() > 0.1:
            return
        
        online_nodes = [
            n for n in self.node_map.values()
            if n['properties'].get('status') == 'online' and not n['properties'].get('is_passive', False)
        ]
        if not online_nodes:
            return

        target_node = random.choice(online_nodes)
        target_node_id = target_node['properties']['id']
        sequence = ATTACK_PATTERNS['brute_force_ssh']['sequence'] if random.random() < 0.2 else [
            random.choice(["Failed network login", "Firewall block"])]

        for event_type in sequence:
            event = {
                "id": f"evt-{uuid.uuid4()}",
                "target_node_id": target_node_id,
                "type": event_type,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "description": f"{event_type} on {target_node_id} from IP 103.42.5.11"
            }
            new_incident_info = self.threat_correlator.add_event(event)
            if new_incident_info:
                summary = await generate_incident_summary(new_incident_info.pop('events'))
                new_incident_info['summary'] = summary
                await self._broadcast_update("new_incident", new_incident_info)

            await self._broadcast_update("security_event", event)
            await asyncio.sleep(random.uniform(0.5, 1.5))

    async def _recalculate_routing_and_broadcast(self):
        active_graph = self.graph.to_undirected()
        for node_id, status in self.simulation_state.get('device_status', {}).items():
            if status != 'online' and active_graph.has_node(node_id):
                active_graph.remove_node(node_id)
        
        paths = {}
        core_node = "core-router-berlin"
        for node in self.node_map.values():
            if node['properties'].get('type') == 'ONT' and self.simulation_state.get('device_status', {}).get(node['properties']['id']) == 'online':
                node_id = node['properties']['id']
                if active_graph.has_node(node_id) and active_graph.has_node(core_node):
                    try:
                        paths[node_id] = nx.shortest_path(active_graph, source=node_id, target=core_node, weight='weight')
                    except nx.NetworkXNoPath:
                        paths[node_id] = []
        await self._broadcast_update("routing_update", {"paths": paths})

    async def update_device_status(self, device_id: str, new_status: str, actor: str = "System", is_cascaded: bool = False):
        node = self.get_node_by_id(device_id)
        if not node or node['properties'].get('status') == new_status:
            return

        # Set the status for the current node
        node['properties']['status'] = new_status
        self.simulation_state['device_status'][device_id] = new_status
        source_actor = "Cascaded" if is_cascaded else actor
        print(f"Status von {device_id} auf {new_status} geändert durch {source_actor}.")
        await self._broadcast_update("node_update", {"id": device_id, "status": new_status})

        # If a device goes offline, all its descendants should also go offline.
        if new_status in ['offline', 'rebooting']:
            if self.graph.has_node(device_id):
                descendants = nx.descendants(self.graph, device_id)
                for descendant_id in descendants:
                    # Use a task to avoid blocking the current update
                    asyncio.create_task(self.update_device_status(descendant_id, new_status, actor, is_cascaded=True))
        
        await self._recalculate_routing_and_broadcast()


    async def reboot_device(self, device_id: str, actor: str):
        async def _reboot():
            await self.update_device_status(device_id, "rebooting", actor)
            await asyncio.sleep(8)
            # Only bring this device back online, descendants are not affected by this final step
            await self.update_device_status(device_id, "online", "System")

        task = asyncio.create_task(_reboot())
        self.background_tasks.add(task)
        task.add_done_callback(self.background_tasks.discard)

    def get_cli_output(self, device_id: str, command: str) -> str:
        node = self.get_node_by_id(device_id)
        if not node:
            return f"Error: Device {device_id} not found."
        
        if node['properties'].get('is_passive', False):
            return f"Error: {device_id} is a passive device. No CLI access available."

        template_id = node['properties'].get('template_id')
        if not template_id:
            return "Error: Unknown device type without plugin reference."

        template = self.plugin_manager.get_template(template_id)
        if not template:
            return f"Error: No plugin for template '{template_id}' found."

        command_output = template.get('cli_commands', {}).get(command.strip().lower())
        if command_output:
            return command_output

        if "show version" in command:
            fw = node['properties'].get('details', {}).get('firmware', {})
            return f"--- {node['properties'].get('label', device_id)} ---\nOS: {fw.get('os', 'N/A')}\nVersion: {fw.get('version', 'N/A')}"

        return f"Error: Unrecognized command '{command}' on this device."

    def get_field_check_results(self, device_id: str) -> dict:
        node = self.get_node_by_id(device_id)
        if not node or not node['properties'].get('is_passive', False):
            return {"error": f"{device_id} is not a valid passive device."}

        if random.random() < 0.1: # 10% chance of a simulated fault
            result = {
                "check_status": "Fault Detected",
                "details": "High insertion loss on fiber 5 (green). Suspected bad splice.",
                "measured_loss_db": round(random.uniform(0.3, 0.8), 2),
                "recommendation": "Re-splice fiber or check connector for contamination."
            }
        else:
            result = {
                "check_status": "Nominal",
                "details": "All fibers and connections within tolerance.",
                "measured_loss_db": round(random.uniform(0.05, 0.2), 2),
                "recommendation": "No action required."
            }
        return result

    async def reset_security_events(self):
        print("Setze Sicherheits-Events zurück...")
        self.threat_correlator.event_buffer = []
        self.threat_correlator.incidents_created = set()
        await self._broadcast_update("clear_security_state", {})