import asyncio
from fastapi import FastAPI, WebSocket, Request
from fastapi.middleware.cors import CORSMiddleware

# Router-Importe (NEU: sandbox!)
from app.routers import auth, users, topology, simulation_actions, forensics, scenarios, devices, sandbox

app = FastAPI(
    title="UltraNOC - Digital Twin Edition",
    version="3.1.0",
    description="Das Backend für die hyperrealistische Unified Operations Platform."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    from app.simulation.simulation_engine import SimulationEngine
    sim_engine = SimulationEngine()
    app.state.sim_engine = sim_engine

    loop = asyncio.get_event_loop()
    app.state.simulation_task = loop.create_task(sim_engine.run_simulation_loop())
    print("Simulations-Engine im Hintergrund gestartet.")

@app.on_event("shutdown")
async def shutdown_event():
    if hasattr(app.state, 'simulation_task'):
        app.state.simulation_task.cancel()
    if hasattr(app.state, 'sim_engine'):
        await app.state.sim_engine.save_state()
    print("Simulations-Engine gestoppt und Zustand gespeichert.")

@app.websocket("/ws/live-updates")
async def websocket_endpoint(websocket: WebSocket):
    sim_engine = websocket.app.state.sim_engine
    await sim_engine.manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        sim_engine.manager.disconnect(websocket)

@app.middleware("http")
async def sim_engine_middleware(request: Request, call_next):
    if hasattr(app.state, 'sim_engine'):
        request.state.sim_engine = app.state.sim_engine
    response = await call_next(request)
    return response

# API-Router einbinden
api_prefix = "/api/v1"
app.include_router(auth.router, prefix=f"{api_prefix}/auth", tags=["Authentication"])
app.include_router(users.router, prefix=f"{api_prefix}/users", tags=["Users"])
app.include_router(topology.router, prefix=f"{api_prefix}/topology", tags=["Topology"])
app.include_router(simulation_actions.router, prefix=f"{api_prefix}/simulation", tags=["Simulation Actions"])
app.include_router(forensics.router, prefix=f"{api_prefix}/forensics", tags=["Forensics"])
app.include_router(scenarios.router, prefix=f"{api_prefix}/scenarios", tags=["Scenarios"])
app.include_router(devices.router, prefix=f"{api_prefix}/devices", tags=["Devices"])
app.include_router(sandbox.router, prefix=f"{api_prefix}/sandbox", tags=["Sandbox"])   # <-- NEU

@app.get("/")
def read_root():
    return {"status": "UltraNOC Backend is running"}