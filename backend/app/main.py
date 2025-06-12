from fastapi import FastAPI
from app.routers import cli, devices, topology, users, alarms, tickets, simulation
from app.simulation import nat  # <- NAT-Router importieren
from app.simulation import failover  # <- Import
from app.simulation import live_flow
from app.routers import roles

app = FastAPI(title="UltraNOC API")

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

