from fastapi import FastAPI
from app.routers import cli, devices, topology, users, alarms, tickets, simulation

app = FastAPI(title="UltraNOC API")

app.include_router(cli.router, prefix="/api/v1/cli")
app.include_router(devices.router, prefix="/api/v1/devices")
app.include_router(topology.router, prefix="/api/v1/topology")
app.include_router(users.router, prefix="/api/v1/users")
app.include_router(alarms.router, prefix="/api/v1/alarms")
app.include_router(tickets.router, prefix="/api/v1/tickets")
app.include_router(simulation.router, prefix="/api/v1/simulation")
