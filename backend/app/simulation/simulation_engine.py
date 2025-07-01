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

class SimulationEngine:
    def __init__(self):
        self.plugin_manager = PluginManager()
        self.topology_data = self._load_json("app/data/sandbox_topology.json") or {"type": "FeatureCollection", "features": []}
        self.simulation_state = self._load_json("app/data/state.json", default={
            "device_status": {}, "link_status": {}, "device_metrics": {}, "metrics_history": {}
        })
        self._initialize_simulation_components()

    def _initialize_simulation_components(self):
        self.manager = ConnectionManager()
        self.background_tasks = set()
        self.threat_correlator = ThreatCorrelator()
        self.security_simulation_enabled = True
        features = self.topology_data.get('features', [])
        self.node_map = {
            node['properties']['id']: node
            for node in features
            if node.get('geometry', {}).get('type') == 'Point' and node.get('properties', {}).get('id')
        }
        self.graph = nx.DiGraph()
        self._build_network_graph()
        self._apply_initial_state()
        print(f"Simulation components initialized/reloaded with {len(self.node_map)} nodes.")

    def reload_topology(self, file_path: str):
        print(f"Reloading topology from {file_path}...")
        self.topology_data = self._load_json(file_path) or {"type": "FeatureCollection", "features": []}
        self._initialize_simulation_components()

    def _load_json(self, file_path, default=None):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and 'type' in data and 'features' in data:
                    return data
                return default
        except (FileNotFoundError, json.JSONDecodeError):
            if default is None:
                default = {"type": "FeatureCollection", "features": []}
            with open(file_path, "w", encoding="utf-8") as f_create:
                json.dump(default, f_create)
            return default

    def get_node_by_id(self, node_id):
        return self.node_map.get(node_id)

    def get_full_topology(self):
        features = self.topology_data.get('features', [])
        for feature in features:
            if feature.get('geometry', {}).get('type') == 'Point':
                props = feature.get('properties', {})
                if 'id' in props:
                    props['status'] = self.simulation_state.get('device_status', {}).get(props['id'], 'unknown')
        return {"type": "FeatureCollection", "features": features}

    def _build_network_graph(self):
        self.graph.clear()
        features = self.topology_data.get('features', [])
        for feature in features:
            if feature.get('geometry', {}).get('type') == 'Point' and feature.get('properties', {}).get('id'):
                self.graph.add_node(feature['properties']['id'])
        for feature in features:
            if feature.get('geometry', {}).get('type') == 'LineString':
                props = feature.get('properties', {})
                source, target = props.get('source'), props.get('target')
                if source and target and self.graph.has_node(source) and self.graph.has_node(target):
                    self.graph.add_edge(source, target, weight=props.get('details', {}).get('length_km', 1))

    def _apply_initial_state(self):
        # Ensure every node has a default status in the simulation state
        for node_id in self.node_map:
            if node_id not in self.simulation_state.get('device_status', {}):
                self.simulation_state['device_status'][node_id] = 'online'
        # Apply status from state to the main topology data
        for feature in self.topology_data.get('features', []):
            if feature.get('geometry', {}).get('type') == 'Point':
                props = feature.get('properties', {})
                if 'id' in props:
                    props['status'] = self.simulation_state['device_status'].get(props['id'], 'unknown')

    async def run_simulation_loop(self):
        while True:
            if self.node_map:
                await asyncio.gather(
                    self._simulate_live_metrics(),
                    self._simulate_cgnat_logging(),
                    self._simulate_security_incidents()
                )
            await asyncio.sleep(5)

    # --- Alle weiteren Methoden (API, Device, CLI, FieldCheck usw.) ---
    # --- Als stabil gekennzeichnet, hier kurz als Dummy für Übersicht ---
    async def _broadcast_update(self, event_type: str, data: dict): await self.manager.broadcast({"type": event_type, "payload": data})
    async def _simulate_live_metrics(self): pass
    async def _simulate_cgnat_logging(self): pass
    async def _simulate_security_incidents(self): pass
    async def update_device_status(self, device_id: str, new_status: str, actor: str = "System", is_cascaded: bool = False): pass
    async def reboot_device(self, device_id: str, actor: str): pass
    def get_cli_output(self, device_id: str, command: str) -> str: return "CLI output stable."
    def get_field_check_results(self, device_id: str) -> dict: return {"check_status": "Nominal"}
