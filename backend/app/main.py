from fastapi import FastAPI
from app.routers import cli, devices, topology, users, alarms, tickets, simulation
from app.simulation import nat  # <- NAT-Router importieren
from app.simulation import failover  # <- Import
from app.simulation import live_flow
from app.routers import roles
from app.routers import scenarios, fiber_types
from app.routers import network_quality
from app.routers import grafik_export
from app.routers import audit_log, vlans
from app.routers import session_data
from app.routers import user_preferences, topology_meta
from app.routers import alerting, maintenance
from app.routers import dns_lookup, syslog_collector
from app.routers import device_ports, topomap_preview, ipv6_tools
from app.routers import cgnat_lookup, maintenance_schedule, system_probe
from app.routers import event_trigger, ping_simulator, snapshot_handler
from app.routers import cgnat_pool, device_inventory, topo_export
from app.routers import device_health, scheduled_tasks, incident_summary
from app.routers import cable_diagnostics, access_log, interface_stats
from app.routers import device_telemetry, ping_tool, flow_archive
from app.routers import license_check, ws_telemetry, cli_playback
from app.routers import auth 
from app.routers import device_metrics
from app.routers import config_store
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="UltraNOC API")

# CORS für Frontend-Freigabe
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routerregistrierungen
app.include_router(cli.router, prefix="/api/v1/cli")
app.include_router(devices.router, prefix="/api/v1/devices")
app.include_router(topology.router, prefix="/api/v1/topology")
app.include_router(users.router, prefix="/api/v1/users")
app.include_router(alarms.router, prefix="/api/v1/alarms")
app.include_router(tickets.router, prefix="/api/v1/tickets")
app.include_router(simulation.router, prefix="/api/v1/simulation")
app.include_router(nat.router, prefix="/api/v1/simulation/nat", tags=["NAT"])  # <- NAT-Router einbinden
app.include_router(failover.router, prefix="/api/v1/simulation/failover", tags=["Failover"])  # <- Router einbinden
app.include_router(live_flow.router, prefix="/api/v1/simulation/live", tags=["Traffic"])
app.include_router(roles.router, prefix="/api/v1/roles", tags=["Roles"])
app.include_router(scenarios.router, prefix="/api/v1/scenario", tags=["Scenarios"])
app.include_router(fiber_types.router, prefix="/api/v1/fiber", tags=["Fiber"])
app.include_router(network_quality.router, prefix="/api/v1/network", tags=["Quality"])
app.include_router(grafik_export.router, prefix="/api/v1/export", tags=["Export"])
app.include_router(audit_log.router, prefix="/api/v1/audit", tags=["Audit"])
app.include_router(vlans.router, prefix="/api/v1/vlans", tags=["VLANs"])
app.include_router(session_data.router, prefix="/api/v1/sessions", tags=["Sessions"])
app.include_router(user_preferences.router, prefix="/api/v1/preferences", tags=["Preferences"])
app.include_router(topology_meta.router, prefix="/api/v1/topology", tags=["Metadata"])
app.include_router(alerting.router, prefix="/api/v1/alerts", tags=["Alerts"])
app.include_router(maintenance.router, prefix="/api/v1/maintenance", tags=["Maintenance"])
app.include_router(dns_lookup.router, prefix="/api/v1/tools/dns", tags=["DNS"])
app.include_router(syslog_collector.router, prefix="/api/v1/syslog", tags=["Syslog"])
app.include_router(device_ports.router, prefix="/api/v1/devices", tags=["Ports"])
app.include_router(topomap_preview.router, prefix="/api/v1/topology", tags=["Preview"])
app.include_router(ipv6_tools.router, prefix="/api/v1/tools/ipv6", tags=["IPv6"])
app.include_router(cgnat_lookup.router, prefix="/api/v1/cgnat", tags=["CGNAT"])
app.include_router(maintenance_schedule.router, prefix="/api/v1/maintenance", tags=["Schedule"])
app.include_router(system_probe.router, prefix="/api/v1/system", tags=["Health"])
app.include_router(event_trigger.router, prefix="/api/v1/events", tags=["Events"])
app.include_router(ping_simulator.router, prefix="/api/v1/tools", tags=["Ping"])
app.include_router(snapshot_handler.router, prefix="/api/v1/snapshots", tags=["Snapshots"])
app.include_router(cgnat_pool.router, prefix="/api/v1/cgnat", tags=["CGNAT"])
app.include_router(device_inventory.router, prefix="/api/v1/inventory", tags=["Inventory"])
app.include_router(topo_export.router, prefix="/api/v1/topology/export", tags=["Topology Export"])
app.include_router(device_health.router, prefix="/api/v1/devices/health", tags=["Device Health"])
app.include_router(scheduled_tasks.router, prefix="/api/v1/scheduler", tags=["Scheduler"])
app.include_router(incident_summary.router, prefix="/api/v1/incidents", tags=["Incidents"])
app.include_router(cable_diagnostics.router, prefix="/api/v1/cables/diagnostics", tags=["Cables"])
app.include_router(access_log.router, prefix="/api/v1/logs", tags=["Access Logs"])
app.include_router(interface_stats.router, prefix="/api/v1/interfaces", tags=["Interface Stats"])
app.include_router(device_telemetry.router, prefix="/api/v1/telemetry", tags=["Telemetry"])
app.include_router(ping_tool.router, prefix="/api/v1/tools", tags=["Ping Tool"])
app.include_router(flow_archive.router, prefix="/api/v1/archive", tags=["Flow Archive"])
app.include_router(license_check.router, prefix="/api/v1/license", tags=["License"])
app.include_router(ws_telemetry.router, tags=["WebSocket"])
app.include_router(cli_playback.router, prefix="/api/v1/playback", tags=["CLI Playback"])
app.include_router(auth.router, prefix="/api/v1/auth") 
app.include_router(device_metrics.router, prefix="/api/v1/metrics", tags=["Metrics"])
app.include_router(config_store.router, prefix="/api/v1/config", tags=["Config Store"])
