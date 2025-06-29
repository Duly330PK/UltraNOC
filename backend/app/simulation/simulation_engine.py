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
            props['status'] = self.simulation_state.get('device_status', {}).get(props['id'], props.get('status', 'unknown'))
    return self.topology_data

def _build_network_graph(self):
    for feature in self.topology_data.get('features', []):
        if feature.get('geometry', {}).get('type') == 'Point':
            self.graph.add_node(feature['properties']['id'])
    for feature in self.topology_data.get('features', []):
        if feature.get('geometry', {}).get('type') == 'LineString':
            props = feature['properties']
            if self.graph.has_node(props['source']) and self.graph.has_node(props['target']):
                self.graph.add_edge(props['source'], props['target'], weight=props.get('length_km', 1))

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
    for feature in self.topology_data.get('features', []):
        props = feature['properties']
        if 'id' in props and 'status' in props:
            self.simulation_state['device_status'][props['id']] = props['status']
        if props.get('source'):
            link_id = f"{props['source']}-{props['target']}"
            self.simulation_state['link_status'][link_id] = props['status']
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
    for node in self.node_map.values():
        props = node['properties']
        if props.get('status') == 'online' and props.get('type') != 'Muffe':
            base_cpu = 15 if "Core" in props.get('type', '') else 5
            cpu = round(random.uniform(base_cpu, base_cpu + 30), 1)
            temp = round(random.uniform(40, 60), 1)
            metrics = {"cpu": cpu, "temp": temp, "timestamp": datetime.now(timezone.utc).isoformat()}
            
            self.simulation_state['device_metrics'][props['id']] = metrics
            history = self.simulation_state['metrics_history'].setdefault(props['id'], [])
            history.append(metrics)
            self.simulation_state['metrics_history'][props['id']] = history[-60:]
            
            metrics_update[props['id']] = {"current": metrics, "history": history[-60:]}
    
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

    if random.random() < 0.1:
        online_nodes = [n for n in self.node_map.values() if n['properties'].get('status') == 'online' and n['properties'].get('type') != 'Muffe']
        if not online_nodes: return
        
        target_node = random.choice(online_nodes)
        target_node_id = target_node['properties']['id']
        
        sequence =  ['brute_force_ssh']['sequence'] if random.random() < 0.2 else [random.choice(["Failed network login", "Firewall block"])]
        
        for event_type in sequence:
            # NEU 2/2: ID-Generierung mit uuid4() für garantierte Einzigartigkeit
            event = {"id": f"evt-{uuid.uuid4()}", "target_node_id": target_node_id, "type": event_type, "timestamp": datetime.now(timezone.utc).isoformat(), "description": f"{event_type} on {target_node_id} from IP 103.42.5.11"}
            new_incident_info = self.threat_correlator.add_event(event)
            if new_incident_info:
                summary = await generate_incident_summary(new_incident_info.pop('events'))
                new_incident_info['summary'] = summary
                await self._broadcast_update("new_incident", new_incident_info)
            
            await self._broadcast_update("security_event", event)
            await asyncio.sleep(random.uniform(0.5, 1.5))

async def _recalculate_routing_and_broadcast(self):
    active_graph = self.graph.copy()
    for feature in self.topology_data['features']:
        if feature['geometry']['type'] == 'Point' and feature['properties']['status'] != 'online':
            if active_graph.has_node(feature['properties']['id']):
                active_graph.remove_node(feature['properties']['id'])
    
    paths = {}
    core_node = "core-router-1"
    for node in self.topology_data['features']:
        if node['geometry']['type'] == 'Point' and node['properties'].get('type') == 'ONT' and node['properties']['status'] == 'online':
            node_id = node['properties']['id']
            if active_graph.has_node(node_id) and active_graph.has_node(core_node):
                try:
                    paths[node_id] = nx.shortest_path(active_graph, source=node_id, target=core_node, weight='weight')
                except nx.NetworkXNoPath:
                    paths[node_id] = []
    
    await self._broadcast_update("routing_update", {"paths": paths})

async def update_device_status(self, device_id: str, new_status: str, actor: str = "System"):
    node = self.get_node_by_id(device_id)
    if node and node['properties']['status'] != new_status:
        # Bestehende Änderung im "Live"-Objekt für die sofortige Anzeige
        node['properties']['status'] = new_status
        
        # NEUE, WICHTIGE ZEILE: Die Änderung im persistenten Simulationszustand speichern
        self.simulation_state['device_status'][device_id] = new_status

        print(f"Status von {device_id} auf {new_status} geändert durch {actor}.")
        await self._broadcast_update("node_update", {"id": device_id, "status": new_status})
        await self._recalculate_routing_and_broadcast()

async def reboot_device(self, device_id: str, actor: str):
    async def _reboot():
        await self.update_device_status(device_id, "rebooting", actor)
        await asyncio.sleep(8)
        await self.update_device_status(device_id, "online", "System")
    
    task = asyncio.create_task(_reboot())
    self.background_tasks.add(task)
    task.add_done_callback(self.background_tasks.discard)

def get_cli_output(self, device_id: str, command: str) -> str:
    node = self.get_node_by_id(device_id)
    if not node: return f"Error: Device {device_id} not found."
    props = node['properties']
    command = command.strip().lower()

    if "show version" in command:
        fw = props.get('details', {}).get('firmware', {})
        return f"--- {props.get('label', device_id)} ---\\nOS: {fw.get('os', 'N/A')}\\nVersion: {fw.get('version', 'N/A')}"
    if "show interface status" in command:
        ifaces = props.get('details', {}).get('interfaces', [])
        if not ifaces: return "No interfaces found."
        header = f"{'Port':<12} | {'Status':<8} | {'VLAN':<8} | {'Description':<20}\\n"
        divider = f"{'-'*12}-+-{'-'*8}-+-{'-'*8}-+-{'-'*20}\\n"
        rows = [f"{p.get('name', ''):<12} | {p.get('status', 'down'):<8} | {p.get('vlan', 'trunk'):<8} | {p.get('desc', ''):<20}" for p in ifaces]
        return header + divider + "\\n".join(rows)
    return f"Error: Unrecognized command '{command}'"

async def reset_security_events(self):
    """Setzt den internen Zustand der Bedrohungserkennung zurück und weist das Frontend an, dasselbe zu tun."""
    print("Setze Sicherheits-Events zurück...")
    self.threat_correlator.event_buffer = []
    self.threat_correlator.incidents_created = set()
    await self._broadcast_update("clear_security_state", {})