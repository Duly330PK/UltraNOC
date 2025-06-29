import asyncio
from fastapi import FastAPI, WebSocket, Request
from fastapi.middleware.cors import CORSMiddleware

# Die Simulation Engine wird später importiert, nachdem die Datei existiert
# from app.simulation.simulation_engine import SimulationEngine

# NEU 1/2: Der 'devices'-Router wird hier importiert
from app.routers import auth, users, topology, simulation_actions, forensics, scenarios, devices

app = FastAPI(
    title="UltraNOC - Digital Twin Edition",
    version="3.0.0",
    description="Das Backend für die hyperrealistische Unified Operations Platform.",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS Middleware für die Kommunikation mit dem React-Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Der Import und die Initialisierung der Engine erfolgen hier, um Zirkel-Importe zu vermeiden
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
    # Der Zugriff auf die sim_engine erfolgt sicher über den App-State
    sim_engine = websocket.app.state.sim_engine
    await sim_engine.manager.connect(websocket)
    try:
        while True:
            # Einfach offen halten, um Updates zu pushen. Ein Timeout könnte hier sinnvoll sein.
            await websocket.receive_text()
    except Exception:
        sim_engine.manager.disconnect(websocket)

# Wrapper, um die sim_engine an die Router zu übergeben
# Dies ist eine saubere Methode, um Abhängigkeiten zu verwalten.
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.sim_engine = app.state.sim_engine
    response = await call_next(request)
    return response

# Einbinden der API-Router
api_prefix = "/api/v1"
app.include_router(auth.router, prefix=f"{api_prefix}/auth", tags=["Authentication"])
app.include_router(users.router, prefix=f"{api_prefix}/users", tags=["Users"])
app.include_router(topology.router, prefix=f"{api_prefix}/topology", tags=["Topology"])
app.include_router(simulation_actions.router, prefix=f"{api_prefix}/simulation", tags=["Simulation Actions"])
app.include_router(forensics.router, prefix=f"{api_prefix}/forensics", tags=["Forensics"])
app.include_router(scenarios.router, prefix=f"{api_prefix}/scenarios", tags=["Scenarios"])

# NEU 2/2: Die neue API für die Geräteliste wird hier eingebunden
app.include_router(devices.router, prefix=f"{api_prefix}/devices", tags=["Devices"])

@app.get("/")
def read_root():
    return {"status": "UltraNOC Backend is running"}