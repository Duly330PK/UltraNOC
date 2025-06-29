import os
import textwrap

# ==============================================================================
# ULTRA NOC - DIGITAL TWIN EDITION - GENESIS SCRIPT (MASTERPLAN)
#
# Dieses Skript erstellt das gesamte UltraNOC-Projekt, inklusive aller
# Backend- und Frontend-Dateien sowie der Docker-Konfiguration.
#
# ANLEITUNG:
# 1. Fügen Sie die Code-Blöcke aus den folgenden Nachrichten in die
#    `PROJECT_FILES`-Liste unten ein.
# 2. Führen Sie das Skript am Ende mit `python create_ultranoc.py` aus.
# ==============================================================================

# Diese Liste wird in den nächsten Schritten mit dem gesamten Projektcode gefüllt.
PROJECT_FILES = [
    ('docker-compose.yml', """
    services:
      db:
        image: postgres:15-alpine
        container_name: ultranoc_db
        environment:
          POSTGRES_USER: root
          POSTGRES_PASSWORD: root
          POSTGRES_DB: ultranoc
        ports:
          - "5432:5432"
        volumes:
          - postgres_data:/var/lib/postgresql/data
        healthcheck:
          test: ["CMD-SHELL", "pg_isready -U root -d ultranoc"]
          interval: 10s
          timeout: 5s
          retries: 5

      backend:
        build:
          context: ./backend
          dockerfile: Dockerfile
        container_name: ultranoc_backend
        ports:
          - "8000:8000"
        volumes:
          - ./backend:/app
        depends_on:
          db:
            condition: service_healthy
        environment:
          - DATABASE_URL=postgresql://root:root@db/ultranoc
          - SECRET_KEY=dein-super-geheimer-schluessel-fuer-jwt-tokens-der-sehr-lang-sein-sollte
          - ALGORITHM=HS256
          - ACCESS_TOKEN_EXPIRE_MINUTES=60
          - LLM_API_URL=http://host.docker.internal:11434/api/generate

      frontend:
        build:
          context: ./frontend
          dockerfile: Dockerfile
        container_name: ultranoc_frontend
        ports:
          - "5173:5173"
        volumes:
          - ./frontend:/app
          - /app/node_modules
        depends_on:
          - backend

    volumes:
      postgres_data:
    """),    ('backend/Dockerfile', """
    FROM python:3.11-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    COPY . .
    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
    """),    ('backend/requirements.txt', """
    fastapi
    uvicorn[standard]
    sqlalchemy
    psycopg2-binary
    passlib[bcrypt]
    python-jose[cryptography]
    python-dotenv
    websockets
    aiofiles
    networkx
    httpx
    """),    ('frontend/Dockerfile', """
    FROM node:18-alpine
    WORKDIR /app
    COPY package*.json ./
    RUN npm install
    COPY . .
    EXPOSE 5173
    # Das '--host' Flag ist wichtig, damit der Vite-Server von außerhalb des Containers erreichbar ist.
    CMD ["npm", "run", "dev", "--", "--host"]
    """),    ('backend/initial_setup.py', """
    import os
    import sys
    import time
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
    from dotenv import load_dotenv

    # Warten auf die Datenbank, um Race Conditions beim ersten Start im Docker-Compose zu vermeiden
    print("Warte 5 Sekunden auf die Datenbank...")
    time.sleep(5)

    # Füge das 'app'-Verzeichnis zum Python-Pfad hinzu, damit die Module gefunden werden
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

    from app.database import Base
    from app.models.user import User
    from app.models.cgnat_log import CGNATLog
    from app.models.security_event import Incident, SecurityEvent
    from app.auth.auth_handler import get_password_hash

    load_dotenv()

    # Verwende die DATABASE_URL aus den Umgebungsvariablen, die von Docker Compose gesetzt wird
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL ist nicht gesetzt. Stelle sicher, dass die Umgebungsvariable korrekt übergeben wird.")

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def check_db_connection():
        retries = 5
        while retries > 0:
            try:
                with engine.connect() as connection:
                    connection.execute(text("SELECT 1"))
                print("Datenbankverbindung erfolgreich hergestellt.")
                return True
            except Exception as e:
                print(f"Warte auf Datenbank... verbleibende Versuche: {retries-1}. Fehler: {e}")
                retries -= 1
                time.sleep(5)
        return False

    def initialize_database():
        if not check_db_connection():
            print("Konnte keine Verbindung zur Datenbank herstellen. Abbruch.")
            return
            
        print("Initialisiere Datenbank-Tabellen...")
        try:
            # Erstelle alle Tabellen, die von `Base` erben
            Base.metadata.create_all(bind=engine)
            print("Tabellen erfolgreich erstellt.")
        except Exception as e:
            print(f"Fehler beim Erstellen der Tabellen: {e}")
            return

        db = SessionLocal()
        try:
            # Füge den Admin-Benutzer hinzu, falls er noch nicht existiert
            if not db.query(User).filter(User.username == "admin").first():
                print("Admin-Benutzer wird erstellt...")
                hashed_password = get_password_hash("admin123")
                admin = User(username="admin", hashed_password=hashed_password, role="admin")
                db.add(admin)
                db.commit()
                print("Admin-Benutzer 'admin' mit Passwort 'admin123' erstellt.")
            else:
                print("Admin-Benutzer existiert bereits.")
        finally:
            db.close()

    if __name__ == "__main__":
        initialize_database()
    """),    ('backend/app/main.py', """
    import asyncio
    from fastapi import FastAPI, WebSocket, Request
    from fastapi.middleware.cors import CORSMiddleware

    # Die Simulation Engine wird später importiert, nachdem die Datei existiert
    # from app.simulation.simulation_engine import SimulationEngine
    
    from app.routers import auth, users, topology, simulation_actions, forensics, scenarios

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

    @app.get("/")
    def read_root():
        return {"status": "UltraNOC Backend is running"}
    """),    ('backend/app/database.py', """
    import os
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.ext.declarative import declarative_base
    from dotenv import load_dotenv

    load_dotenv()

    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable not set.")

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    """),    ('backend/app/models/__init__.py', """
    from app.database import Base
    from .user import User
    from .cgnat_log import CGNATLog
    from .security_event import Incident, SecurityEvent
    """),    ('backend/app/models/user.py', """
    from sqlalchemy import Column, String, Text
    from sqlalchemy.dialects.postgresql import UUID
    from app.database import Base
    import uuid

    class User(Base):
        __tablename__ = "users"
        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="Eindeutige ID des Benutzers")
        username = Column(String(100), unique=True, index=True, nullable=False, comment="Benutzername für den Login")
        hashed_password = Column(String(255), nullable=False, comment="BCrypt-gehashtes Passwort")
        role = Column(String(50), default="user", nullable=False, comment="Benutzerrolle (z.B. admin, operator, viewer)")
    """),    ('backend/app/models/cgnat_log.py', """
    from sqlalchemy import Column, String, Integer, DateTime, BigInteger
    from app.database import Base
    from datetime import datetime, timezone

    class CGNATLog(Base):
        __tablename__ = 'cgnat_session_map'
        session_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True, comment="Eindeutige ID der NAT-Session")
        timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True, comment="Startzeitpunkt der Session (UTC)")
        duration = Column(Integer, default=300, comment="Dauer der Session in Sekunden")
        customer_id = Column(String(100), index=True, comment="Interne Kundenkennung")
        internal_ip = Column(String(45), comment="Private IP des Kunden (z.B. aus 100.64.0.0/10)")
        internal_port = Column(Integer, comment="Privater Port des Kunden")
        external_ip = Column(String(45), index=True, comment="Öffentliche IP des CGNAT-Gateways")
        external_port = Column(Integer, index=True, comment="Gemappter öffentlicher Port")
        protocol = Column(String(4), comment="Protokoll (TCP/UDP)")
        segment = Column(String(20), nullable=True, comment="Optionales internes Routing-Segment oder Tunnel-ID")
    """),  ('backend/app/models/security_event.py', """
    from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON, Text
    from sqlalchemy.orm import relationship
    from app.database import Base
    from datetime import datetime, timezone

    class Incident(Base):
        __tablename__ = 'incidents'
        id = Column(Integer, primary_key=True, index=True, comment="Eindeutige ID des Sicherheitsvorfalls")
        title = Column(String(255), index=True, comment="Titel des Incidents (z.B. 'Brute-Force-Angriff')")
        description = Column(Text, comment="Vom LLM generierte Zusammenfassung des Vorfalls")
        status = Column(String(50), default="Pending", comment="Status: Pending, In Progress, Resolved, Closed")
        assignee = Column(String(100), nullable=True, comment="Zugewiesener Analyst")
        created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
        events = relationship("SecurityEvent", back_populates="incident", cascade="all, delete-orphan")

    class SecurityEvent(Base):
        __tablename__ = 'security_events'
        id = Column(Integer, primary_key=True, index=True, comment="Eindeutige ID des Sicherheitsereignisses")
        incident_id = Column(Integer, ForeignKey('incidents.id'), nullable=True, comment="Zugehöriger Incident, falls korreliert")
        timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
        type = Column(String(100), comment="Art des Ereignisses (z.B. 'Failed SSH login')")
        description = Column(Text, comment="Detaillierte Beschreibung des Events")
        source_ip = Column(String(45), nullable=True, comment="Quell-IP des Ereignisses")
        target_node_id = Column(String(100), nullable=True, comment="Zielgerät des Ereignisses")
        details = Column(JSON, nullable=True, comment="Zusätzliche Metadaten als JSON-Objekt")
        incident = relationship("Incident", back_populates="events")
    """),    ('backend/app/auth/auth_handler.py', """
    import os
    from datetime import datetime, timedelta, timezone
    from typing import Optional
    from jose import JWTError, jwt
    from passlib.context import CryptContext
    from dotenv import load_dotenv

    load_dotenv()

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    def decode_access_token(token: str) -> Optional[dict]:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            return None
    """),    ('backend/app/auth/auth_bearer.py', """
    from fastapi import Depends, HTTPException, status
    from fastapi.security import OAuth2PasswordBearer
    from sqlalchemy.orm import Session
    from app.database import get_db
    from app.models.user import User
    from app.auth.auth_handler import decode_access_token

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

    def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
        payload = decode_access_token(token)
        if not payload or "sub" not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        username: str = payload["sub"]
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user

    def require_role(required_role: str):
        def role_checker(current_user: User = Depends(get_current_user)) -> User:
            # Simple role check. For multiple roles, logic would be more complex.
            if current_user.role != required_role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"User does not have the required '{required_role}' role"
                )
            return current_user
        return role_checker
    """),    ('backend/app/schemas/__init__.py', """
    # This file makes the 'schemas' directory a Python package.
    """),    ('backend/app/schemas/user_schema.py', """
    from pydantic import BaseModel, Field
    import uuid

    class UserBase(BaseModel):
        username: str

    class UserCreate(UserBase):
        password: str = Field(..., min_length=8)
        role: str = "user"

    class UserResponse(UserBase):
        id: uuid.UUID
        role: str

        class Config:
            from_attributes = True
    """),    ('backend/app/schemas/auth_schema.py', """
    from pydantic import BaseModel

    class TokenSchema(BaseModel):
        access_token: str
        token_type: str = "bearer"
    """),    ('backend/app/schemas/forensics_schema.py', """
    from pydantic import BaseModel
    from datetime import datetime

    class ForensicsQuery(BaseModel):
        ip_address: str
        port: int
        timestamp: datetime

    class ForensicsResult(BaseModel):
        found: bool
        customer_id: str | None = None
        internal_ip: str | None = None
        segment: str | None = None
        device_id: str | None = None
    """),    ('backend/app/schemas/scenario_schema.py', """
    from pydantic import BaseModel
    from typing import List

    class Scenario(BaseModel):
        name: str
        description: str
        steps: List[dict]
    """),    ('backend/app/routers/__init__.py', """
    # This file makes the 'routers' directory a Python package.
    """),    ('backend/app/routers/auth.py', """
    from fastapi import APIRouter, Depends, HTTPException, status
    from fastapi.security import OAuth2PasswordRequestForm
    from sqlalchemy.orm import Session
    from app.database import get_db
    from app.models.user import User
    from app.schemas.auth_schema import TokenSchema
    from app.auth.auth_handler import create_access_token, verify_password

    router = APIRouter()

    @router.post("/login", response_model=TokenSchema)
    def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
        user = db.query(User).filter(User.username == form_data.username).first()
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": user.username, "role": user.role})
        return TokenSchema(access_token=access_token)
    """),    ('backend/app/routers/users.py', """
    from fastapi import APIRouter, Depends
    from sqlalchemy.orm import Session
    from typing import List
    from app.database import get_db
    from app.models.user import User
    from app.schemas.user_schema import UserResponse
    from app.auth.auth_bearer import require_role

    router = APIRouter()

    @router.get("/", response_model=List[UserResponse], dependencies=[Depends(require_role("admin"))])
    def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        users = db.query(User).offset(skip).limit(limit).all()
        return users
    """),    ('backend/app/routers/topology.py', """
    from fastapi import APIRouter, Depends, Request
    from app.auth.auth_bearer import get_current_user
    from app.models.user import User

    router = APIRouter()

    @router.get("/")
    def get_topology(request: Request, current_user: User = Depends(get_current_user)):
        sim_engine = request.app.state.sim_engine
        return sim_engine.get_full_topology()
    """),    ('backend/app/routers/forensics.py', """
    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy.orm import Session
    from app.database import get_db
    from app.schemas.forensics_schema import ForensicsQuery, ForensicsResult
    from app.models.cgnat_log import CGNATLog
    from app.models.user import User
    from datetime import timedelta, timezone
    from app.auth.auth_bearer import require_role

    router = APIRouter(dependencies=[Depends(require_role("admin"))])

    @router.post("/trace", response_model=ForensicsResult)
    def trace_connection(query: ForensicsQuery, db: Session = Depends(get_db)):
        # Ensure timestamp from frontend is timezone-aware (UTC) for correct comparison
        if query.timestamp.tzinfo is None:
            query.timestamp = query.timestamp.replace(tzinfo=timezone.utc)
            
        time_window_start = query.timestamp - timedelta(minutes=5)
        time_window_end = query.timestamp + timedelta(minutes=5)

        log_entry = db.query(CGNATLog).filter(
            CGNATLog.external_ip == query.ip_address,
            CGNATLog.external_port == query.port,
            CGNATLog.timestamp.between(time_window_start, time_window_end)
        ).order_by(CGNATLog.timestamp.desc()).first()

        if not log_entry:
            raise HTTPException(status_code=404, detail="No matching log entry found for the given time window.")

        # In a real system, this would involve a lookup in a provisioning database.
        # Here, we simulate it based on the customer ID format.
        simulated_device_id = f"ONT-{log_entry.customer_id[-4:]}"

        return ForensicsResult(
            found=True,
            customer_id=log_entry.customer_id,
            internal_ip=log_entry.internal_ip,
            segment=log_entry.segment,
            device_id=simulated_device_id
        )
    """),    ('backend/app/routers/simulation_actions.py', """
    from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Request
    from app.auth.auth_bearer import get_current_user
    from app.models.user import User

    router = APIRouter()

    @router.post("/devices/{device_id}/action", status_code=202)
    async def perform_device_action(
        device_id: str,
        action: dict,
        request: Request,
        background_tasks: BackgroundTasks,
        user: User = Depends(get_current_user)
    ):
        sim_engine = request.app.state.sim_engine
        action_type = action.get("type")
        payload = action.get("payload", {})
        
        if not sim_engine.get_node_by_id(device_id):
            raise HTTPException(status_code=404, detail=f"Device {device_id} not found.")

        actor = f"User '{user.username}'"

        if action_type == "set_status":
            new_status = payload.get("status")
            if not new_status:
                raise HTTPException(status_code=400, detail="Status not provided")
            # Using background_tasks to run the async function without blocking the response
            background_tasks.add_task(sim_engine.update_device_status, device_id, new_status, actor)
            return {"message": f"Task to set status for {device_id} to {new_status} started."}
            
        elif action_type == "reboot":
            background_tasks.add_task(sim_engine.reboot_device, device_id, actor)
            return {"message": f"Reboot sequence for {device_id} initiated."}
            
        elif action_type == "get_cli_output":
            command = payload.get("command")
            if not command:
                raise HTTPException(status_code=400, detail="Command not provided")
            output = sim_engine.get_cli_output(device_id, command)
            return {"output": output}

        raise HTTPException(status_code=400, detail="Invalid action type")
    """),    ('backend/app/routers/scenarios.py', """
    import json
    import asyncio
    from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Request
    from app.auth.auth_bearer import require_role

    router = APIRouter(dependencies=[Depends(require_role("admin"))])

    def _load_scenario(name: str):
        try:
            # Construct a safe path to the scenarios directory
            # This prevents directory traversal attacks
            base_path = "app/data/scenarios"
            safe_name = name.replace("..", "").replace("/", "").replace("\\\\", "")
            file_path = f"{base_path}/{safe_name}.json"
            
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail=f"Szenario '{name}' nicht gefunden.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Szenario-Datei konnte nicht gelesen werden: {e}")

    async def _execute_scenario(sim_engine, steps: list):
        for step in steps:
            await asyncio.sleep(step.get("delay_s", 1))
            action = step.get("action")
            target_id = step.get("target_id")
            payload = step.get("payload")

            if not all([action, target_id, payload]):
                print(f"Skipping invalid step in scenario: {step}")
                continue
            
            if action == "set_status":
                await sim_engine.update_device_status(target_id, payload.get("status"), "Scenario")
            # Here, more actions for scenarios could be implemented in the future.

    @router.post("/load/{scenario_name}", status_code=202)
    async def load_scenario(scenario_name: str, request: Request, background_tasks: BackgroundTasks):
        sim_engine = request.app.state.sim_engine
        scenario_data = _load_scenario(scenario_name)
        background_tasks.add_task(_execute_scenario, sim_engine, scenario_data.get("steps", []))
        return {"message": f"Szenario '{scenario_data.get('name', 'Unbenannt')}' wurde gestartet."}
    """),    ('backend/app/simulation/__init__.py', """
    # This file makes the 'simulation' directory a Python package.
    """),    ('backend/app/simulation/connection_manager.py', """
    from fastapi import WebSocket
    from typing import List
    import json

    class ConnectionManager:
        def __init__(self):
            self.active_connections: List[WebSocket] = []

        async def connect(self, websocket: WebSocket):
            await websocket.accept()
            self.active_connections.append(websocket)

        def disconnect(self, websocket: WebSocket):
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)

        async def broadcast(self, message: dict):
            # Erstelle eine Kopie, um Thread-Safety-Probleme bei Verbindungsabbrüchen zu vermeiden
            # während der Iteration.
            connections = self.active_connections[:]
            for connection in connections:
                try:
                    await connection.send_text(json.dumps(message))
                except Exception:
                    # Verbindung könnte bereits geschlossen sein, entferne sie sicher
                    self.disconnect(connection)
    """),    ('backend/app/simulation/threat_correlator.py', """
    from datetime import datetime, timedelta, timezone
    from typing import List, Dict, Optional

    # Definiert einfache Angriffsmuster als Sequenz von Ereignistypen.
    # In einem echten System wäre dies eine komplexe, externe Konfiguration.
    ATTACK_PATTERNS = {
        "brute_force_ssh": {
            "name": "Potenzieller Brute-Force SSH-Angriff",
            "sequence": ["Failed SSH login", "Failed SSH login", "Failed SSH login", "Successful SSH login"],
            "time_window_seconds": 300, # Angriff muss innerhalb von 5 Minuten erfolgen
        }
        # Hier könnten weitere Muster definiert werden, z.B. für Port-Scans etc.
    }

    class ThreatCorrelator:
        '''
        Diese Klasse analysiert einen Strom von Sicherheitsereignissen und versucht,
        bekannte Angriffsmuster zu erkennen.
        '''
        def __init__(self):
            # Ein Buffer, der die letzten relevanten Sicherheitsereignisse speichert.
            self.event_buffer: List[Dict] = []
            # Ein Set, um bereits gemeldete Incidents zu speichern und Duplikate zu vermeiden.
            self.incidents_created = set()

        def add_event(self, event: Dict) -> Optional[Dict]:
            '''Fügt ein neues Event hinzu und prüft sofort auf bekannte Muster.'''
            self.event_buffer.append(event)
            
            # Bereinige den Buffer von alten Events, um die Performance zu gewährleisten.
            now = datetime.fromisoformat(event["timestamp"])
            if now.tzinfo is None:
                now = now.replace(tzinfo=timezone.utc)
            
            self.event_buffer = [
                e for e in self.event_buffer 
                if now - datetime.fromisoformat(e["timestamp"]).replace(tzinfo=timezone.utc) < timedelta(seconds=600)
            ]
            return self.check_for_patterns()

        def check_for_patterns(self) -> Optional[Dict]:
            '''Prüft den Event-Buffer auf vordefinierte Angriffsmuster.'''
            # Gruppiere Events nach dem Zielgerät, um Angriffe auf ein spezifisches Ziel zu erkennen.
            events_on_target = {}
            for event in self.event_buffer:
                target = event.get('target_node_id')
                if target:
                    events_on_target.setdefault(target, []).append(event)

            for target, events in events_on_target.items():
                event_types = [e['type'] for e in events]
                for pattern_key, pattern in ATTACK_PATTERNS.items():
                    # Einfache Sequenzprüfung: Prüft, ob die Mustersequenz in den Ereignissen enthalten ist.
                    pattern_str = ",".join(pattern["sequence"])
                    events_str = ",".join(event_types)
                    
                    if pattern_str in events_str:
                        # Erzeuge eine eindeutige ID für diesen Incident, um ihn nicht mehrfach zu melden.
                        incident_id = f"inc-{pattern_key}-{target}"
                        if incident_id not in self.incidents_created:
                            print(f"!!! NEUER VORFALL ENTDECKT: {pattern['name']} auf {target} !!!")
                            self.incidents_created.add(incident_id)
                            
                            # Gib die relevanten Informationen für die Incident-Erstellung zurück.
                            relevant_events = [e for e in events if e['type'] in pattern['sequence']]
                            return {"name": pattern['name'], "target": target, "events": relevant_events}
            return None
    """),    ('backend/app/llm_gateway.py', """
    import httpx
    import os
    from typing import List, Dict

    LLM_API_URL = os.getenv("LLM_API_URL", "http://host.docker.internal:11434/api/generate")

    async def generate_text_with_history(prompt: str, history: List[Dict[str, str]] = None) -> str:
        # Erstellt einen formatierten Prompt, der den Chat-Verlauf berücksichtigt,
        # um dem LLM Kontext zu geben.
        full_prompt = ""
        if history:
            for entry in history:
                # Formatierung für ChatML-basierte Modelle wie Mistral Instruct
                full_prompt += f"<|im_start|>{entry['role']}\\n{entry['content']}<|im_end|>\\n"
        full_prompt += f"<|im_start|>user\\n{prompt}<|im_end|>\\n<|im_start|>assistant\\n"

        # Das zu verwendende Modell sollte idealerweise konfigurierbar sein.
        # Für die Demo verwenden wir 'mistral:instruct' als Annahme.
        payload = {"model": "mistral:instruct", "prompt": full_prompt, "stream": False}

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(LLM_API_URL, json=payload)
                response.raise_for_status()
                return response.json().get("response", "LLM-Antwort konnte nicht verarbeitet werden.").strip()
            except httpx.RequestError:
                return f"Fehler: LLM Gateway nicht erreichbar. Läuft Ollama/LM Studio unter {LLM_API_URL} und ist das Modell 'mistral:instruct' geladen?"
            except Exception as e:
                return f"Ein unerwarteter Fehler ist aufgetreten: {e}"

    async def generate_incident_summary(events: List[Dict]) -> str:
        event_summary = "\\n".join([f"- {e['timestamp']}: {e['description']}" for e in events])
        prompt = f'''
        Du bist ein Cybersecurity-Analyst. Fasse die folgende Kette von Ereignissen zu einem professionellen Incident-Bericht zusammen.
        Erkenne das Muster, gib dem Vorfall einen aussagekräftigen Namen und beschreibe kurz den potenziellen Angriffsvektor.
        
        Ereignis-Kette:
        {event_summary}
        
        Zusammenfassung des Vorfalls:
        '''
        return await generate_text_with_history(prompt)
    """),    ('backend/app/simulation/simulation_engine.py', """
    import json
    import asyncio
    import random
    import aiofiles
    import networkx as nx
    from datetime import datetime, timezone
    from app.simulation.connection_manager import ConnectionManager
    from app.simulation.threat_correlator import ThreatCorrelator
    from app.llm_gateway import generate_incident_summary
    from app.database import SessionLocal
    from app.models.cgnat_log import CGNATLog

    class SimulationEngine:
        def __init__(self):
            self.topology_data = self._load_json("app/data/full_topology.json")
            self.simulation_state = self._load_json("app/data/state.json", default={"device_status": {}, "link_status": {}, "device_metrics": {}, "metrics_history": {}})
            self.manager = ConnectionManager()
            self.background_tasks = set()
            self.threat_correlator = ThreatCorrelator()
            
            self.node_map = {node['properties']['id']: node for node in self.topology_data.get('features', []) if node.get('geometry', {}).get('type') == 'Point'}
            
            self.graph = nx.Graph()
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
            # Stellt sicher, dass der 'status' immer aktuell ist
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
            if random.random() < 0.1:
                online_nodes = [n for n in self.node_map.values() if n['properties'].get('status') == 'online' and n['properties'].get('type') != 'Muffe']
                if not online_nodes: return
                
                target_node = random.choice(online_nodes)
                target_node_id = target_node['properties']['id']
                
                sequence = ATTACK_PATTERNS['brute_force_ssh']['sequence'] if random.random() < 0.2 else [random.choice(["Failed network login", "Firewall block"])]
                
                for event_type in sequence:
                    event = {"id": f"evt-{int(datetime.now(timezone.utc).timestamp()) + random.randint(0,1000)}","target_node_id": target_node_id, "type": event_type, "timestamp": datetime.now(timezone.utc).isoformat(), "description": f"{event_type} on {target_node_id} from IP 103.42.5.11"}
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
                node['properties']['status'] = new_status
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
    """),    ('backend/app/data/state.json', """
    {
        "device_status": {},
        "link_status": {},
        "device_metrics": {},
        "metrics_history": {}
    }
    """),    ('backend/app/data/scenarios/ddos_attack.json', """
    {
        "name": "DDoS-Angriff auf Core-Router",
        "description": "Simuliert einen DDoS-Angriff, der die CPU-Last des Core-Routers erhöht und zu Paketverlust führt. Dies wird durch wiederholte Statusänderungen simuliert, die Alarme auslösen.",
        "steps": [
            { "delay_s": 2, "action": "set_status", "target_id": "core-router-1", "payload": {"status": "warning"} },
            { "delay_s": 5, "action": "set_status", "target_id": "core-router-1", "payload": {"status": "critical"} }
        ]
    }
    """),    ('backend/app/data/scenarios/insider_threat.json', """
    {
        "name": "Insider-Bedrohung: Falsche Konfiguration",
        "description": "Ein simulierter Techniker schaltet bei Wartungsarbeiten versehentlich einen wichtigen Uplink des Core-Routers ab, was zu einem Routing-Failover führen sollte. Nach kurzer Zeit wird der Fehler bemerkt und korrigiert.",
        "steps": [
            { "delay_s": 1, "action": "set_status", "target_id": "olt-1", "payload": {"status": "maintenance"} },
            { "delay_s": 3, "action": "set_status", "target_id": "core-router-1", "payload": {"status": "offline"} },
            { "delay_s": 10, "action": "set_status", "target_id": "core-router-1", "payload": {"status": "online"} },
            { "delay_s": 2, "action": "set_status", "target_id": "olt-1", "payload": {"status": "online"} }
        ]
    }
    """),    ('frontend/package.json', """
    {
      "name": "ultranoc-frontend",
      "private": true,
      "version": "3.0.0",
      "type": "module",
      "scripts": {
        "dev": "vite",
        "build": "vite build",
        "preview": "vite preview"
      },
      "dependencies": {
        "@react-three/drei": "^9.105.4",
        "@react-three/fiber": "^8.16.2",
        "cmdk": "^1.0.0",
        "leaflet": "^1.9.4",
        "lucide-react": "^0.378.0",
        "react": "^18.2.0",
        "react-dom": "^18.2.0",
        "react-leaflet": "^4.2.1",
        "react-router-dom": "^6.23.1",
        "recharts": "^2.12.6",
        "three": "^0.164.1"
      },
      "devDependencies": {
        "@vitejs/plugin-react": "^4.2.1",
        "autoprefixer": "^10.4.19",
        "postcss": "^8.4.38",
        "tailwindcss": "^3.4.3",
        "vite": "^5.2.0"
      }
    }
    """),    ('frontend/vite.config.js', """
    import { defineConfig } from 'vite';
    import react from '@vitejs/plugin-react';
    import path from 'path';

    export default defineConfig({
      plugins: [react()],
      server: {
        port: 5173,
        host: true, // Wichtig für Docker
        proxy: {
          '/api': {
            target: 'http://backend:8000', // Docker-interner Service-Name
            changeOrigin: true,
          },
           '/ws': {
            target: 'ws://backend:8000', // WebSocket-Proxy
            ws: true,
          },
        }
      },
      resolve: {
        alias: {
          "@": path.resolve(__dirname, "./src"),
        }
      }
    });
    """),    ('frontend/tailwind.config.js', """
    /** @type {import('tailwindcss').Config} */
    export default {
      content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
      ],
      theme: {
        extend: {
          colors: {
            'noc-dark': '#0d1117',
            'noc-light-dark': '#161b22',
            'noc-border': '#30363d',
            'noc-text': '#c9d1d9',
            'noc-text-secondary': '#8b949e',
            'noc-blue': '#58a6ff',
            'noc-green': '#3fb950',
            'noc-yellow': '#d29922',
            'noc-red': '#f85149',
            'noc-purple': '#a371f7',
          },
        },
      },
      plugins: [],
    }
    """),    ('frontend/postcss.config.js', """
    export default {
      plugins: {
        tailwindcss: {},
        autoprefixer: {},
      },
    }
    """),    ('frontend/index.html', """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <link rel="icon" type="image/svg+xml" href="/logo.svg" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>UltraNOC - Unified Operations Platform</title>
      </head>
      <body class="bg-noc-dark">
        <div id="root"></div>
        <script type="module" src="/src/main.jsx"></script>
      </body>
    </html>
    """),    ('frontend/public/logo.svg', """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="#58a6ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M2 17L12 22L22 17" stroke="#58a6ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M2 12L12 17L22 12" stroke="#58a6ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    """),    ('frontend/src/index.css', """
    @tailwind base;
    @tailwind components;
    @tailwind utilities;

    .leaflet-container {
        background-color: #0d1117 !important;
    }
    .leaflet-control-zoom-in, .leaflet-control-zoom-out {
        background-color: #161b22 !important;
        color: #c9d1d9 !important;
        border-color: #30363d !important;
    }
    .leaflet-tooltip {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        color: #c9d1d9 !important;
    }
    """),    ('frontend/src/main.jsx', """
    import React from 'react';
    import ReactDOM from 'react-dom/client';
    import { BrowserRouter } from 'react-router-dom';
    import App from './App.jsx';
    import './index.css';
    import { AuthProvider } from './contexts/AuthContext.jsx';
    import { TopologyProvider } from './contexts/TopologyContext.jsx';
    import { CommandMenuProvider } from './contexts/CommandMenuContext.jsx';

    ReactDOM.createRoot(document.getElementById('root')).render(
      <React.StrictMode>
        <BrowserRouter>
          <AuthProvider>
            <TopologyProvider>
              <CommandMenuProvider>
                <App />
              </CommandMenuProvider>
            </TopologyProvider>
          </AuthProvider>
        </BrowserRouter>
      </React.StrictMode>
    );
    """),    ('frontend/src/App.jsx', """
    import React, { useContext, useEffect } from 'react';
    import { Routes, Route, Navigate } from 'react-router-dom';
    import Layout from './layout/Layout';
    import ProtectedRoute from './components/auth/ProtectedRoute';
    import LoginPage from './pages/LoginPage';
    import DashboardPage from './pages/DashboardPage';
    import TopologyPage from './pages/TopologyPage';
    import IncidentsPage from './pages/IncidentsPage';
    import ForensicsPage from './pages/ForensicsPage';
    import Topology3DPage from './pages/Topology3DPage';
    import CommandMenu from './components/shared/CommandMenu';
    import { CommandMenuContext } from './contexts/CommandMenuContext';
    import { AuthContext } from './contexts/AuthContext';

    function App() {
      const { toggleCommandMenu } = useContext(CommandMenuContext);
      const { logout } = useContext(AuthContext);

      useEffect(() => {
        const handleKeyDown = (e) => {
          if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
            e.preventDefault();
            toggleCommandMenu();
          }
        };

        const handleLogout = () => {
          logout();
        }

        document.addEventListener('keydown', handleKeyDown);
        // Custom event listener to allow logout from anywhere in the app
        window.addEventListener('logout-request', handleLogout);

        return () => {
          document.removeEventListener('keydown', handleKeyDown);
          window.removeEventListener('logout-request', handleLogout);
        };
      }, [toggleCommandMenu, logout]);

      return (
        <>
          <CommandMenu />
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
              <Route index element={<Navigate to="/dashboard" replace />} />
              <Route path="dashboard" element={<DashboardPage />} />
              <Route path="topology" element={<TopologyPage />} />
              <Route path="topology-3d" element={<Topology3DPage />} />
              <Route path="incidents" element={<IncidentsPage />} />
              <Route path="incidents/:id" element={<IncidentsPage />} />
              <Route path="forensics" element={<ForensicsPage />} />
            </Route>
            <Route path="*" element={<Navigate to="/login" replace />} />
          </Routes>
        </>
      );
    }

    export default App;
    """),    ('frontend/src/api/auth.js', """
    export const loginUser = async (username, password) => {
        const response = await fetch('/api/v1/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ username, password }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Login failed');
        }
        return response.json();
    };
    """),    ('frontend/src/contexts/AuthContext.jsx', """
    import React, { createContext, useState } from 'react';
    import { useNavigate } from 'react-router-dom';
    import { loginUser } from '../api/auth';

    export const AuthContext = createContext();

    export const AuthProvider = ({ children }) => {
        const [token, setToken] = useState(localStorage.getItem('ultranoc_token'));
        const navigate = useNavigate();

        const login = async (username, password) => {
            const data = await loginUser(username, password);
            localStorage.setItem('ultranoc_token', data.access_token);
            setToken(data.access_token);
            navigate('/dashboard');
        };

        const logout = () => {
            localStorage.removeItem('ultranoc_token');
            setToken(null);
            navigate('/login', { replace: true });
        };

        const authContextValue = {
            token,
            login,
            logout,
            isAuthenticated: !!token,
        };

        return (
            <AuthContext.Provider value={authContextValue}>
                {children}
            </AuthContext.Provider>
        );
    };
    """),    ('frontend/src/contexts/TopologyContext.jsx', """
    import React, { createContext, useState, useEffect, useCallback, useContext } from 'react';
    import { AuthContext } from './AuthContext';
    import L from 'leaflet';

    export const TopologyContext = createContext();

    export const TopologyProvider = ({ children }) => {
        const [topology, setTopology] = useState({ type: "FeatureCollection", features: [] });
        const [liveMetrics, setLiveMetrics] = useState({ current: {}, history: {} });
        const [incidents, setIncidents] = useState([]);
        const [securityEvents, setSecurityEvents] = useState([]);
        const [selectedElement, setSelectedElement] = useState(null);
        const [tracedPath, setTracedPath] = useState(null);
        const [mapBounds, setMapBounds] = useState(null);
        const { isAuthenticated, token, logout } = useContext(AuthContext);

        const fetchTopology = useCallback(async () => {
            if (!token) return;
            try {
                const response = await fetch('/api/v1/topology/', {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if(response.ok) {
                    const data = await response.json();
                    setTopology(data);
                    if (data.features && data.features.length > 0) {
                        const bounds = L.geoJSON(data).getBounds();
                        if (bounds.isValid()) {
                            setMapBounds(bounds);
                        }
                    }
                } else if (response.status === 401) {
                    console.error("Auth error, logging out.");
                    logout();
                }
            } catch (error) {
                console.error("Fehler beim Laden der Topologie:", error);
            }
        }, [token, logout]);

        useEffect(() => {
            if (!isAuthenticated) return;

            fetchTopology();

            const connectWebSocket = () => {
                const socket = new WebSocket(`ws://${window.location.host}/ws/live-updates`);
                
                socket.onopen = () => console.log("WebSocket-Verbindung geöffnet.");
                socket.onclose = () => {
                    console.log("WebSocket-Verbindung geschlossen. Erneuter Verbindungsversuch in 5s.");
                    setTimeout(connectWebSocket, 5000);
                };
                socket.onerror = (error) => console.error("WebSocket-Fehler: ", error);

                socket.onmessage = (event) => {
                    const message = JSON.parse(event.data);
                    const { type, payload } = message;

                    if (type === 'node_update') {
                        setTopology(prev => ({
                            ...prev,
                            features: prev.features.map(f => {
                                if (f.geometry.type === 'Point' && f.properties.id === payload.id) {
                                    return { ...f, properties: { ...f.properties, status: payload.status } };
                                }
                                return f;
                            })
                        }));
                        setSelectedElement(prev => (prev && prev.properties.id === payload.id ? {...prev, properties: {...prev.properties, status: payload.status}} : prev));
                    }
                    if (type === 'link_update') {
                        setTopology(prev => ({
                            ...prev,
                            features: prev.features.map(f => {
                                if (f.geometry.type === 'LineString' && f.properties.source === payload.source && f.properties.target === payload.target) {
                                    return { ...f, properties: { ...f.properties, status: payload.status } };
                                }
                                return f;
                            })
                        }));
                    }
                    if (type === 'metrics_update') {
                        setLiveMetrics(prev => ({
                            current: { ...prev.current, ...payload },
                            history: Object.keys(payload).reduce((acc, nodeId) => {
                                acc[nodeId] = payload[nodeId].history;
                                return acc;
                            }, { ...prev.history })
                        }));
                    }
                    if (type === 'security_event') {
                        setSecurityEvents(prev => [payload, ...prev].slice(0, 100));
                    }
                    if (type === 'new_incident') {
                        setIncidents(prev => [payload, ...prev]);
                    }
                };
                return () => { if (socket.readyState === 1) socket.close(); };
            };

            const cleanup = connectWebSocket();
            return cleanup;
        }, [isAuthenticated, fetchTopology]);

        const selectElement = (element, trace = false) => {
            setSelectedElement(element);
            setTracedPath(null);
            if (trace && element?.properties?.id) {
                // In einer echten App würde der Pfad vom Backend kommen
                const path = ["core-router-1", "olt-1", element.properties.id];
                setTracedPath(path);
            }
        };

        const clearSelection = () => {
            setSelectedElement(null);
            setTracedPath(null);
        };

        const traceAndShowOnMap = (deviceId) => {
            const node = topology.features.find(f => f.properties.id === deviceId);
            if (node) {
                selectElement(node, true);
            }
        };

        const value = {
            topology, liveMetrics, incidents, securityEvents,
            selectedElement, tracedPath, selectElement, clearSelection,
            traceAndShowOnMap, mapBounds
        };

        return <TopologyContext.Provider value={value}>{children}</TopologyContext.Provider>;
    };
    """),    ('frontend/src/contexts/CommandMenuContext.jsx', """
    import React, { createContext, useState } from 'react';

    export const CommandMenuContext = createContext();

    export const CommandMenuProvider = ({ children }) => {
        const [isOpen, setOpen] = useState(false);

        const toggleCommandMenu = () => {
            setOpen(prev => !prev);
        };

        return (
            <CommandMenuContext.Provider value={{ isOpen, setOpen, toggleCommandMenu }}>
                {children}
            </CommandMenuContext.Provider>
        );
    };
    """),    ('frontend/src/layout/Layout.jsx', """
    import React, { useContext } from 'react';
    import { Outlet, NavLink } from 'react-router-dom';
    import { AuthContext } from '../contexts/AuthContext';
    import { CommandMenuContext } from '../contexts/CommandMenuContext';
    import { BarChart2, Compass, Globe, Shield, Search, LogOut, TerminalSquare } from 'lucide-react';

    const navItems = [
        { path: '/dashboard', label: 'Dashboard', icon: <BarChart2 size={18} /> },
        { path: '/topology', label: '2D-Topologie', icon: <Compass size={18} /> },
        { path: '/topology-3d', label: '3D-Topologie', icon: <Globe size={18} /> },
        { path: '/incidents', label: 'Incidents', icon: <Shield size={18} /> },
        { path: '/forensics', label: 'Forensik', icon: <Search size={18} /> },
    ];

    const Layout = () => {
        const { logout } = useContext(AuthContext);
        const { toggleCommandMenu } = useContext(CommandMenuContext);

        return (
            <div className="flex h-screen bg-noc-dark text-noc-text">
                {/* Sidebar */}
                <aside className="w-64 bg-noc-light-dark flex-shrink-0 flex flex-col border-r border-noc-border">
                    <div className="h-16 flex items-center justify-center text-xl font-bold border-b border-noc-border">
                        <img src="/logo.svg" alt="UltraNOC Logo" className="h-8 w-8 mr-2" />
                        UltraNOC
                    </div>
                    <nav className="flex-1 px-2 py-4 space-y-1">
                        {navItems.map((item) => (
                            <NavLink
                                key={item.path}
                                to={item.path}
                                className={({ isActive }) =>
                                    `flex items-center gap-3 px-3 py-2 text-noc-text-secondary rounded-md text-sm font-medium
                                    hover:bg-noc-border hover:text-noc-text transition-colors duration-200 
                                    ${isActive ? 'bg-noc-blue text-white' : ''}`
                                }
                            >
                                {item.icon}
                                <span>{item.label}</span>
                            </NavLink>
                        ))}
                    </nav>
                    <div className="px-2 py-4 border-t border-noc-border space-y-2">
                         <button
                            onClick={toggleCommandMenu}
                            className="w-full flex items-center gap-3 px-3 py-2 text-noc-text-secondary rounded-md text-sm font-medium
                                    hover:bg-noc-border hover:text-noc-text transition-colors duration-200"
                        >
                            <TerminalSquare size={18} />
                            <span>Befehlsmenü</span>
                            <kbd className="ml-auto text-xs border border-noc-border rounded px-1.5 py-0.5">Ctrl+K</kbd>
                        </button>
                        <button
                            onClick={logout}
                            className="w-full flex items-center gap-3 px-3 py-2 text-noc-text-secondary rounded-md text-sm font-medium
                                    hover:bg-noc-red hover:text-white transition-colors duration-200"
                        >
                            <LogOut size={18} />
                            <span>Logout</span>
                        </button>
                    </div>
                </aside>

                {/* Main Content */}
                <div className="flex-1 flex flex-col overflow-hidden">
                    <main className="flex-1 overflow-x-hidden overflow-y-auto bg-noc-dark">
                        <Outlet />
                    </main>
                </div>
            </div>
        );
    };

    export default Layout;
    """),    ('frontend/src/components/auth/ProtectedRoute.jsx', """
    import React, { useContext } from 'react';
    import { Navigate, useLocation } from 'react-router-dom';
    import { AuthContext } from '../../contexts/AuthContext';

    const ProtectedRoute = ({ children }) => {
        const { isAuthenticated } = useContext(AuthContext);
        const location = useLocation();

        if (!isAuthenticated) {
            // Leite zur Login-Seite weiter und speichere die ursprüngliche Route,
            // damit der Benutzer nach dem Login dorthin zurückkehren kann.
            return <Navigate to="/login" state={{ from: location }} replace />;
        }

        return children;
    };

    export default ProtectedRoute;
    """),    ('frontend/src/components/shared/CommandMenu.jsx', """
    import React, { useContext, useEffect } from 'react';
    import { Command } from 'cmdk';
    import { CommandMenuContext } from '../../contexts/CommandMenuContext';
    import { useNavigate } from 'react-router-dom';
    import { BarChart2, Compass, Shield, Search, LogOut, Globe } from 'lucide-react';

    export default function CommandMenu() {
        const { isOpen, setOpen } = useContext(CommandMenuContext);
        const navigate = useNavigate();

        // Schließt das Menü bei einem Routenwechsel
        useEffect(() => {
            if (isOpen) {
                const handleRouteChange = () => setOpen(false);
                // Ein einfacher Weg, um auf Navigation zu hören.
                // In komplexeren Apps könnte dies über den Router-Kontext erfolgen.
                window.addEventListener('popstate', handleRouteChange);
                return () => window.removeEventListener('popstate', handleRouteChange);
            }
        }, [isOpen, setOpen, navigate]);

        const runCommand = (command) => {
            setOpen(false);
            command();
        };

        const commandItems = [
            { 
                heading: "Navigation", 
                items: [
                    { label: "Dashboard", action: () => navigate('/dashboard'), icon: <BarChart2 size={16}/> },
                    { label: "Topologie (2D)", action: () => navigate('/topology'), icon: <Compass size={16}/> },
                    { label: "Topologie (3D)", action: () => navigate('/topology-3d'), icon: <Globe size={16}/> },
                    { label: "Incidents", action: () => navigate('/incidents'), icon: <Shield size={16}/> },
                    { label: "Forensik", action: () => navigate('/forensics'), icon: <Search size={16}/> },
                ]
            },
            { 
                heading: "Aktionen", 
                items: [
                    { 
                        label: "Logout", 
                        // Wir verwenden ein Custom Event, um die Logout-Funktion aus dem AuthContext aufzurufen,
                        // da wir hier keinen direkten Zugriff darauf haben.
                        action: () => window.dispatchEvent(new CustomEvent('logout-request')), 
                        icon: <LogOut size={16}/> 
                    }
                ]
            }
        ];

        if (!isOpen) return null;

        return (
            <Command.Dialog open={isOpen} onOpenChange={setOpen} label="Global Command Menu">
                 <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50" onClick={() => setOpen(false)} />
                 <div className="fixed top-[20vh] left-1/2 -translate-x-1/2 w-full max-w-xl z-50">
                    <div className="bg-noc-light-dark text-noc-text border border-noc-border rounded-lg shadow-lg">
                        <Command.Input 
                            placeholder="Befehl oder Seite suchen..."
                            className="w-full text-lg bg-transparent p-4 border-b border-noc-border outline-none" 
                        />
                        <Command.List className="p-2 max-h-[400px] overflow-y-auto">
                            <Command.Empty>Keine Ergebnisse gefunden.</Command.Empty>
                            {commandItems.map((group) => (
                               <Command.Group key={group.heading} heading={group.heading} className="text-xs text-noc-text-secondary px-2 py-1 uppercase tracking-wider">
                                    {group.items.map(item => (
                                        <Command.Item 
                                            key={item.label}
                                            onSelect={item.action ? () => runCommand(item.action) : undefined}
                                            className="flex items-center gap-3 p-3 rounded-md hover:bg-noc-border cursor-pointer aria-selected:bg-noc-blue aria-selected:text-white"
                                        >
                                            {item.icon}
                                            <span className="text-base text-noc-text">{item.label}</span>
                                        </Command.Item>
                                    ))}
                               </Command.Group>
                            ))}
                        </Command.List>
                    </div>
                </div>
            </Command.Dialog>
        );
    }
    """),    ('frontend/src/pages/LoginPage.jsx', """
    import React, { useState, useContext } from 'react';
    import { AuthContext } from '../contexts/AuthContext';
    import { Navigate } from 'react-router-dom';

    const LoginPage = () => {
        const [username, setUsername] = useState('admin');
        const [password, setPassword] = useState('admin123');
        const [error, setError] = useState('');
        const [isLoading, setIsLoading] = useState(false);
        const { login, isAuthenticated } = useContext(AuthContext);

        const handleLogin = async (e) => {
            e.preventDefault();
            setError('');
            setIsLoading(true);
            try {
                await login(username, password);
            } catch (err) {
                setError(err.message || 'Login fehlgeschlagen. Bitte überprüfen Sie Ihre Zugangsdaten.');
            } finally {
                setIsLoading(false);
            }
        };

        if (isAuthenticated) {
            return <Navigate to="/dashboard" />;
        }

        return (
            <div className="flex items-center justify-center min-h-screen bg-noc-dark">
                <div className="w-full max-w-sm p-8 space-y-8 bg-noc-light-dark rounded-lg shadow-lg border border-noc-border">
                    <div className="text-center">
                        <img src="/logo.svg" alt="UltraNOC Logo" className="w-16 h-16 mx-auto mb-4" />
                        <h1 className="text-2xl font-bold text-noc-text">UltraNOC Login</h1>
                        <p className="text-noc-text-secondary">Unified Operations Platform</p>
                    </div>
                    <form className="space-y-6" onSubmit={handleLogin}>
                        <div>
                            <label htmlFor="username" className="sr-only">Username</label>
                            <input
                                id="username"
                                name="username"
                                type="text"
                                autoComplete="username"
                                required
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                className="w-full px-3 py-2 bg-noc-dark border border-noc-border rounded-md placeholder-noc-text-secondary focus:outline-none focus:ring-2 focus:ring-noc-blue"
                                placeholder="Username"
                            />
                        </div>
                        <div>
                            <label htmlFor="password" className="sr-only">Password</label>
                            <input
                                id="password"
                                name="password"
                                type="password"
                                autoComplete="current-password"
                                required
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full px-3 py-2 bg-noc-dark border border-noc-border rounded-md placeholder-noc-text-secondary focus:outline-none focus:ring-2 focus:ring-noc-blue"
                                placeholder="Password"
                            />
                        </div>
                        {error && <p className="text-sm text-noc-red text-center">{error}</p>}
                        <div>
                            <button
                                type="submit"
                                disabled={isLoading}
                                className="w-full py-2 px-4 bg-noc-blue text-white font-semibold rounded-md hover:bg-opacity-80 transition-all disabled:bg-noc-border disabled:cursor-not-allowed"
                            >
                                {isLoading ? 'Signing In...' : 'Sign In'}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        );
    };

    export default LoginPage;
    """),    ('frontend/src/pages/DashboardPage.jsx', """
    import React, { useContext } from 'react';
    import { TopologyContext } from '../contexts/TopologyContext';
    import { AlertCircle, CheckCircle, ShieldAlert, Wifi, Server, Cpu } from 'lucide-react';

    const StatCard = ({ label, value, color, icon }) => (
        <div className="bg-noc-light-dark p-6 rounded-lg border border-noc-border transition-all hover:border-noc-blue hover:shadow-lg">
            <div className="flex items-center gap-4">
                <div className={`p-3 rounded-full bg-opacity-10 ${color}`}>{icon}</div>
                <div>
                    <h3 className="text-sm font-medium text-noc-text-secondary">{label}</h3>
                    <p className={`text-3xl font-semibold mt-1 text-noc-text`}>{value}</p>
                </div>
            </div>
        </div>
    );

    const DashboardPage = () => {
        const { incidents, securityEvents, topology, liveMetrics } = useContext(TopologyContext);

        const onlineDevices = topology.features.filter(f => f.geometry.type === 'Point' && f.properties.status === 'online').length;
        const totalDevices = topology.features.filter(f => f.geometry.type === 'Point').length;
        const avgCpu = Object.keys(liveMetrics.current).length > 0
            ? Object.values(liveMetrics.current).reduce((acc, curr) => acc + curr.cpu, 0) / Object.keys(liveMetrics.current).length
            : 0;

        const stats = [
            { label: "System-Status", value: "Operational", color: "text-noc-green", icon: <CheckCircle /> },
            { label: "Aktive Incidents", value: incidents.length, color: "text-noc-red", icon: <ShieldAlert /> },
            { label: "Sicherheits-Events (letzte Std.)", value: securityEvents.length, color: "text-noc-yellow", icon: <AlertCircle /> },
            { label: "Online-Geräte", value: `${onlineDevices} / ${totalDevices}`, color: "text-noc-blue", icon: <Server /> },
            { label: "Ø CPU-Last", value: `${avgCpu.toFixed(1)}%`, color: "text-noc-purple", icon: <Cpu /> },
        ];

        return (
            <div className="p-4 sm:p-6 lg:p-8">
                <h1 className="text-3xl font-bold text-noc-text mb-6">NOC/SOC Dashboard</h1>
                
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6">
                    {stats.map(stat => (
                        <StatCard key={stat.label} {...stat} />
                    ))}
                </div>

                <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <div className="bg-noc-light-dark p-4 rounded-lg border border-noc-border">
                        <h2 className="text-xl font-bold text-noc-text mb-4 px-2">Letzte Sicherheits-Events</h2>
                        <ul className="text-sm text-noc-text-secondary space-y-2 font-mono h-64 overflow-y-auto">
                            {securityEvents.length > 0 ? securityEvents.slice(0, 10).map(event => (
                                <li key={event.id} className="p-2 rounded-md hover:bg-noc-dark">
                                    <span className="text-noc-yellow">[{new Date(event.timestamp).toLocaleTimeString()}]</span> {event.description}
                                </li>
                            )) : <li className="p-2">Keine Events in der letzten Stunde.</li>}
                        </ul>
                    </div>
                     <div className="bg-noc-light-dark p-4 rounded-lg border border-noc-border">
                        <h2 className="text-xl font-bold text-noc-text mb-4 px-2">Neue Incidents</h2>
                         <ul className="text-sm text-noc-text-secondary space-y-2 h-64 overflow-y-auto">
                            {incidents.length > 0 ? incidents.slice(0, 5).map((incident, index) => (
                                <li key={index} className="p-3 rounded-md hover:bg-noc-dark border-l-2 border-noc-red">
                                    <h3 className="font-bold text-noc-red">{incident.name}</h3>
                                    <p className="text-xs mt-1">{incident.summary}</p>
                                </li>
                            )) : <li className="p-2">Keine neuen Incidents.</li>}
                        </ul>
                    </div>
                </div>
            </div>
        );
    };

    export default DashboardPage;
    """),    ('frontend/src/pages/TopologyPage.jsx', """
    import React, { useContext, useEffect, useMemo } from 'react';
    import { MapContainer, TileLayer, GeoJSON, Tooltip, useMap } from 'react-leaflet';
    import L from 'leaflet';
    import 'leaflet/dist/leaflet.css';
    import { TopologyContext } from '../contexts/TopologyContext';
    import ControlPanel from '../components/topology/ControlPanel';

    // Leaflet Icon Fix für Vite
    delete L.Icon.Default.prototype._getIconUrl;
    L.Icon.Default.mergeOptions({
      iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
      iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
      shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
    });

    const getStatusColor = (status) => {
        switch (status) {
            case 'online': return '#3fb950';
            case 'offline': return '#f85149';
            case 'rebooting':
            case 'updating':
            case 'maintenance':
            case 'warning': return '#d29922';
            default: return '#8b949e';
        }
    };

    const MapController = ({ bounds }) => {
        const map = useMap();
        useEffect(() => {
            if (bounds && bounds.isValid()) {
                map.fitBounds(bounds, { padding: [50, 50] });
            }
        }, [map, bounds]);
        return null;
    }

    const TopologyPage = () => {
        const { topology, selectedElement, selectElement, mapBounds, tracedPath } = useContext(TopologyContext);

        const onEachFeature = (feature, layer) => {
            layer.on({ click: (e) => { L.DomEvent.stopPropagation(e); selectElement(feature); } });
            if(feature.properties?.label) {
                layer.bindTooltip(`<b>${feature.properties.label}</b><br>${feature.properties.type}`);
            }
        };
        
        const styleFeature = (feature) => {
            const props = feature.properties;
            const isNodeSelected = selectedElement?.geometry.type === 'Point' && selectedElement.properties.id === props.id;
            const isLinkSelected = selectedElement?.geometry.type === 'LineString' && selectedElement.properties.source === props.source && selectedElement.properties.target === props.target;
            
            // Prüft, ob ein Knoten oder ein Link Teil des getracten Pfades ist
            let inPath = false;
            if (tracedPath) {
                if (props.id) { // Es ist ein Knoten
                    inPath = tracedPath.includes(props.id);
                } else if (props.source && props.target) { // Es ist ein Link
                    for (let i = 0; i < tracedPath.length - 1; i++) {
                        if ((tracedPath[i] === props.source && tracedPath[i+1] === props.target) || (tracedPath[i] === props.target && tracedPath[i+1] === props.source)) {
                            inPath = true;
                            break;
                        }
                    }
                }
            }

            const baseStyle = getStatusStyle(props.status);
            let style = { color: baseStyle, weight: 3, opacity: 0.9, fillOpacity: 0.8, fillColor: baseStyle };

            if (isNodeSelected || isLinkSelected) {
                style.weight = 5;
                style.color = '#58a6ff';
            }
            if (inPath) {
                style.weight = 6;
                style.color = '#a371f7';
                style.dashArray = '10, 5';
            }
            return style;
        };
        
        const pointToLayer = (feature, latlng) => {
             return L.circleMarker(latlng, {
                ...styleFeature(feature),
                radius: 8,
             });
        };

        const memoizedGeoJSON = useMemo(() => (
            <GeoJSON 
                data={topology} 
                onEachFeature={onEachFeature} 
                pointToLayer={pointToLayer}
                style={styleFeature}
                key={JSON.stringify(topology.features.map(f => f.properties.status))}
            />
        ), [topology, selectedElement, tracedPath]);

        return (
            <div className="flex h-full w-full">
                <div className="flex-grow h-full">
                    <MapContainer center={[51.9607, 7.6261]} zoom={13} style={{ height: '100%', width: '100%' }}>
                        <TileLayer
                            attribution='© <a href="https://carto.com/attributions">CARTO</a>'
                            url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                        />
                        {topology.features.length > 0 && memoizedGeoJSON}
                         <MapController bounds={mapBounds} />
                    </MapContainer>
                </div>
                <div className="w-96 h-full flex-shrink-0">
                    <ControlPanel />
                </div>
            </div>
        );
    };

    export default TopologyPage;
    """),    ('frontend/src/pages/IncidentsPage.jsx', """
    import React, { useContext } from 'react';
    import { TopologyContext } from '../contexts/TopologyContext';
    import SocPanel from '../components/incidents/SocPanel';
    import IncidentGraph from '../components/incidents/IncidentGraph';
    import incidentData from '../data/incident_example.json';

    const IncidentsPage = () => {
        const { incidents } = useContext(TopologyContext);

        // Für die Demo verwenden wir statische Daten, wenn keine dynamischen vorhanden sind
        // In einer echten App würde man hier eine Liste von Incidents darstellen
        // und bei Klick die Detailansicht für den jeweiligen Incident laden.
        const displayIncident = incidents.length > 0 ? {
            ...incidentData, // Nimm die statischen Metriken
            title: incidents[0].name,
            summary: incidents[0].summary
        } : incidentData;

        return (
            <div className="flex h-full w-full p-4 gap-4">
                <div className="flex-grow h-full">
                    <IncidentGraph incident={displayIncident} />
                </div>
                <div className="w-96 h-full flex-shrink-0">
                    <SocPanel incident={displayIncident} />
                </div>
            </div>
        );
    };
    export default IncidentsPage;
    """),    ('frontend/src/pages/ForensicsPage.jsx', """
    import React, { useState, useContext } from 'react';
    import { TopologyContext } from '../contexts/TopologyContext';
    import { useNavigate } from 'react-router-dom';
    import { Search, Clock, Hash } from 'lucide-react';

    const ForensicsPage = () => {
      const [ipAddress, setIpAddress] = useState('91.194.84.73');
      const [port, setPort] = useState('40965');
      const [timestamp, setTimestamp] = useState(new Date().toISOString().slice(0, 16));
      const [result, setResult] = useState(null);
      const [isLoading, setIsLoading] = useState(false);
      const [error, setError] = useState('');
      
      const { traceAndShowOnMap } = useContext(TopologyContext);
      const navigate = useNavigate();

      const handleTrace = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');
        setResult(null);

        const token = localStorage.getItem('ultranoc_token');
        try {
          const response = await fetch('/api/v1/forensics/trace', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify({
              ip_address: ipAddress,
              port: parseInt(port),
              timestamp: new Date(timestamp).toISOString(),
            }),
          });

          if (!response.ok) {
              const errData = await response.json();
              throw new Error(errData.detail || 'Suche fehlgeschlagen.');
          }
          const data = await response.json();
          setResult(data);

        } catch (err) {
          setError(err.message);
        } finally {
          setIsLoading(false);
        }
      };

      const showOnMap = () => {
        if (result && result.found && result.device_id) {
            traceAndShowOnMap(result.device_id);
            navigate('/topology');
        }
      };

      return (
        <div className="p-4 sm:p-6 lg:p-8 h-full flex flex-col text-noc-text">
           <h1 className="text-2xl font-bold mb-4">Forensische Verbindungsanalyse</h1>
           <p className="text-noc-text-secondary mb-6">Verfolgen Sie eine öffentliche IP-Adresse und einen Port zu einem bestimmten Zeitpunkt zurück, um den zugehörigen Kundenanschluss zu identifizieren.</p>
           
           <form onSubmit={handleTrace} className="bg-noc-light-dark p-6 rounded-lg border border-noc-border max-w-2xl">
               <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                 <div>
                   <label htmlFor="ipAddress" className="block text-sm font-medium text-noc-text-secondary mb-1">Öffentliche IP-Adresse</label>
                   <input type="text" id="ipAddress" value={ipAddress} onChange={(e) => setIpAddress(e.target.value)} className="w-full bg-noc-dark border border-noc-border rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-noc-blue" required />
                 </div>
                 <div>
                   <label htmlFor="port" className="block text-sm font-medium text-noc-text-secondary mb-1">Port</label>
                   <input type="number" id="port" value={port} onChange={(e) => setPort(e.target.value)} className="w-full bg-noc-dark border border-noc-border rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-noc-blue" required />
                 </div>
                 <div>
                   <label htmlFor="timestamp" className="block text-sm font-medium text-noc-text-secondary mb-1">Zeitstempel (UTC)</label>
                   <input type="datetime-local" id="timestamp" value={timestamp} onChange={(e) => setTimestamp(e.target.value)} className="w-full bg-noc-dark border border-noc-border rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-noc-blue" required />
                 </div>
               </div>
               <div className="mt-6">
                 <button type="submit" disabled={isLoading} className="w-full flex items-center justify-center gap-2 bg-noc-blue text-white py-2 px-4 rounded-md hover:bg-opacity-80 disabled:bg-noc-border disabled:cursor-not-allowed">
                   <Search size={16} />
                   {isLoading ? 'Suche läuft...' : 'Verbindung verfolgen'}
                 </button>
               </div>
           </form>
           
           {error && <div className="mt-6 p-4 bg-noc-red bg-opacity-20 text-noc-red rounded-md max-w-2xl">{error}</div>}
           
           {result && (
                <div className="mt-6 bg-noc-light-dark p-6 rounded-lg border border-noc-border max-w-2xl">
                    <h2 className="text-xl font-bold mb-4">Analyseergebnis</h2>
                    {result.found ? (
                        <div>
                            <p className="text-noc-green font-bold mb-4">Kundenanschluss erfolgreich identifiziert!</p>
                            <div className="grid grid-cols-2 gap-4 font-mono text-sm">
                                <div className="text-noc-text-secondary">Kunden-ID:</div><div className="text-noc-text">{result.customer_id}</div>
                                <div className="text-noc-text-secondary">Interne IP:</div><div className="text-noc-text">{result.internal_ip}</div>
                                <div className="text-noc-text-secondary">Segment:</div><div className="text-noc-text">{result.segment}</div>
                                <div className="text-noc-text-secondary">Gerät (ONT):</div><div className="text-noc-text">{result.device_id}</div>
                            </div>
                            <button onClick={showOnMap} className="mt-6 bg-noc-green text-white py-2 px-4 rounded-md hover:bg-opacity-80">Auf Karte anzeigen</button>
                        </div>
                    ) : (
                        <p className="text-noc-yellow">Für die angegebenen Daten konnte kein passender Log-Eintrag gefunden werden.</p>
                    )}
                </div>
           )}
        </div>
      );
    };

    export default ForensicsPage;
    """),    ('frontend/src/pages/Topology3DPage.jsx', """
    import React, { Suspense, useContext, useMemo } from 'react';
    import { Canvas } from '@react-three/fiber';
    import { OrbitControls, Text, Line, Sphere } from '@react-three/drei';
    import { TopologyContext } from '../contexts/TopologyContext';

    const Node3D = ({ node }) => {
      const color = node.properties.status === 'online' ? '#3fb950' : '#f85149';
      return (
        <group position={node.position3d}>
          <Sphere args={[0.2, 32, 32]}>
            <meshStandardMaterial color={color} emissive={color} emissiveIntensity={2} toneMapped={false} />
          </Sphere>
          <Text position={[0, 0.4, 0]} fontSize={0.15} color="white" anchorX="center" anchorY="middle">
            {node.properties.label}
          </Text>
        </group>
      );
    };

    const Link3D = ({ startNode, endNode }) => {
      return <Line points={[startNode.position3d, endNode.position3d]} color="gray" lineWidth={1} />;
    };

    const Topology3DPage = () => {
      const { topology } = useContext(TopologyContext);

      const { nodesWith3DPos, links } = useMemo(() => {
        const nodes = topology.features.filter(f => f.geometry.type === 'Point');
        const nodesWith3DPos = nodes.map((node, i) => ({
            ...node,
            position3d: [(i % 6 - 3) * 3, Math.floor(i / 6) * -3, (i % 3 - 1) * 2],
        }));
        
        const nodeMap = Object.fromEntries(nodesWith3DPos.map(n => [n.properties.id, n]));
        const links = topology.features
            .filter(f => f.geometry.type === 'LineString')
            .map(link => ({
                ...link,
                startNode: nodeMap[link.properties.source],
                endNode: nodeMap[link.properties.target]
            }))
            .filter(l => l.startNode && l.endNode);

        return { nodesWith3DPos, links };
      }, [topology]);


      return (
        <div className="h-full w-full bg-noc-dark">
            <div className="absolute top-4 left-4 text-noc-text-secondary z-10 p-2 bg-noc-light-dark/50 rounded-md pointer-events-none">
                Experimentelle 3D-Ansicht. Nutzen Sie die Maus zum Navigieren.
            </div>
            <Canvas camera={{ position: [0, -2, 12], fov: 75 }}>
                <ambientLight intensity={1.5} />
                <pointLight position={[10, 10, 10]} intensity={2.5} />
                <Suspense fallback={null}>
                  {nodesWith3DPos.map(node => <Node3D key={node.properties.id} node={node} />)}
                  {links.map((link, i) => <Link3D key={i} {...link} />)}
                </Suspense>
                <OrbitControls />
            </Canvas>
        </div>
      );
    };

    export default Topology3DPage;
    """),    ('frontend/src/data/incident_example.json', """
    {
      "id": 1,
      "title": "Credential dumping via MimiKats",
      "summary": "Professionally grow e-business web-readiness rather than technically sound metrics. Phosfluorescently foster high standards in schemas for business value.",
      "status": "Pending",
      "assignee": "Cole Bishop",
      "metrics": {
        "events": 195,
        "attackers": "01",
        "victims": "02",
        "artifacts": 23,
        "mitigations": "07",
        "notes": "03"
      },
      "events": [
        { "id": "03", "description": "Successfull SSH login", "time": "18:10" },
        { "id": "04", "description": "Host-base firewall blocked", "time": "14:30" },
        { "id": "09", "description": "Failed SSH login", "time": "18:20" }
      ]
    }
    """),    ('frontend/src/components/topology/ControlPanel.jsx', """
    import React, { useContext, useState, useEffect } from 'react';
    import { TopologyContext } from '../../contexts/TopologyContext';
    import DetailsTab from './tabs/DetailsTab';
    import ActionsTab from './tabs/ActionsTab';
    import TerminalTab from './tabs/TerminalTab';
    import { Network, Server, Cpu, Cable, AlertCircle, Link as LinkIcon, X } from 'lucide-react';

    const getIconForType = (type) => {
        if (!type) return <LinkIcon size={20} />;
        if (type.includes('Router')) return <Server size={20} />;
        if (type.includes('OLT')) return <Cpu size={20} />;
        if (type.includes('Muffe')) return <Cable size={20} />;
        if (type.includes('ONT')) return <Network size={20} />;
        return <AlertCircle size={20} />;
    };

    const ControlPanel = () => {
        const { selectedElement, clearSelection } = useContext(TopologyContext);
        const [activeTab, setActiveTab] = useState('details');

        useEffect(() => {
            if (selectedElement) {
                const props = selectedElement.properties || {};
                const isLink = selectedElement.geometry?.type === 'LineString';
                const isTerminalDisabled = isLink || props.type === 'Muffe';
                if (isTerminalDisabled && activeTab === 'terminal') {
                    setActiveTab('details');
                }
            } else {
                setActiveTab('details');
            }
        }, [selectedElement, activeTab]);

        if (!selectedElement) {
            return (
                <div className="bg-noc-light-dark text-noc-text-secondary rounded-lg border border-noc-border p-6 h-full flex items-center justify-center text-center">
                    <div>
                        <h3 className="font-bold text-noc-text">Kein Element ausgewählt</h3>
                        <p className="text-xs mt-1">Klicken Sie auf einen Knoten oder eine Verbindung auf der Karte, um Details anzuzeigen.</p>
                    </div>
                </div>
            );
        }

        const props = selectedElement.properties;
        const isLink = selectedElement.geometry.type === 'LineString';
        const title = isLink ? `Link: ${props.source} → ${props.target}` : props.label;
        const type = isLink ? props.type : props.type;

        const tabs = [
            { id: 'details', label: 'Details' },
            { id: 'actions', label: 'Aktionen', disabled: isLink },
            { id: 'terminal', label: 'Terminal', disabled: isLink || props.type === 'Muffe' }
        ];

        return (
            <div className="bg-noc-light-dark rounded-lg border border-noc-border h-full flex flex-col">
                <div className="p-4 border-b border-noc-border flex items-center gap-4 relative">
                    <div className="text-noc-blue flex-shrink-0">{getIconForType(type)}</div>
                    <div className="flex-grow min-w-0">
                        <h2 className="text-lg font-bold text-noc-text truncate" title={title}>{title}</h2>
                        <p className="text-sm text-noc-text-secondary">{type}</p>
                    </div>
                    <button onClick={clearSelection} className="absolute top-2 right-2 text-noc-text-secondary hover:text-white p-1 rounded-full hover:bg-noc-border">
                        <X size={16} />
                    </button>
                </div>

                <div className="border-b border-noc-border flex">
                    {tabs.map(tab => !tab.disabled && (
                        <button 
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`flex-1 py-2 text-sm transition-colors duration-150 ${activeTab === tab.id ? 'bg-noc-blue text-white' : 'text-noc-text-secondary hover:bg-noc-border'}`}
                        >
                            {tab.label}
                        </button>
                    ))}
                </div>
                
                <div className="p-4 flex-grow overflow-y-auto">
                    {activeTab === 'details' && <DetailsTab element={selectedElement} />}
                    {activeTab === 'actions' && <ActionsTab element={selectedElement} />}
                    {activeTab === 'terminal' && <TerminalTab element={selectedElement} />}
                </div>
            </div>
        );
    };

    export default ControlPanel;
    """),    ('frontend/src/components/topology/tabs/DetailsTab.jsx', """
    import React, { useContext } from 'react';
    import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
    import { TopologyContext } from '../../../contexts/TopologyContext';

    const DetailRenderer = ({ data, level = 0 }) => {
        if (typeof data !== 'object' || data === null) {
            return <span className="text-noc-blue">{String(data)}</span>;
        }

        return (
            <div style={{ marginLeft: level * 12 }} className="space-y-1">
                {Object.entries(data).map(([key, value]) => (
                    <div key={key}>
                        <span className="text-noc-text-secondary">{key}: </span>
                        {Array.isArray(value) ? (
                            <div className="pl-4 border-l border-noc-border">
                                {value.map((item, index) => <DetailRenderer key={index} data={item} level={level + 1} />)}
                            </div>
                        ) : typeof value === 'object' && value !== null ? (
                            <DetailRenderer data={value} level={level + 1} />
                        ) : (
                            <span className="text-noc-blue font-semibold">{String(value)}</span>
                        )}
                    </div>
                ))}
            </div>
        );
    };

    const LiveMetricGraph = ({ data, dataKey, stroke, unit }) => (
        <ResponsiveContainer width="100%" height={80}>
            <LineChart data={data} margin={{ top: 5, right: 20, left: -10, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#30363d" />
                <XAxis dataKey="timestamp" tickFormatter={(ts) => new Date(ts).toLocaleTimeString()} stroke="#8b949e" tick={{fontSize: 10}} />
                <YAxis stroke="#8b949e" tick={{fontSize: 10}} unit={unit} domain={[0, 'dataMax + 10']}/>
                <Tooltip contentStyle={{ backgroundColor: '#161b22', border: '1px solid #30363d' }} itemStyle={{color: stroke}} labelStyle={{color: '#c9d1d9'}}/>
                <Line type="monotone" dataKey={dataKey} stroke={stroke} strokeWidth={2} dot={false} isAnimationActive={false} />
            </LineChart>
        </ResponsiveContainer>
    );

    const DetailsTab = ({ element }) => {
        const { liveMetrics } = useContext(TopologyContext);
        const elementId = element.properties.id;
        const metricsHistory = liveMetrics.history[elementId] || [];
        const isNode = element.geometry.type === 'Point';

        return (
            <div className="text-sm font-mono whitespace-pre-wrap">
                {isNode && element.properties.type !== 'Muffe' && (
                    <div className="mb-4 p-3 bg-noc-dark rounded-md border border-noc-border">
                       <h4 className="text-md text-noc-text-secondary mb-2 font-sans font-bold">Live Metriken</h4>
                       <div>CPU Auslastung (%)</div>
                       <LiveMetricGraph data={metricsHistory} dataKey="cpu" stroke="#58a6ff" unit="%" />
                       <div>Temperatur (°C)</div>
                       <LiveMetricGraph data={metricsHistory} dataKey="temp" stroke="#d29922" unit="°C" />
                    </div>
                )}
                <h4 className="text-md text-noc-text-secondary mt-4 mb-2 font-sans font-bold">Eigenschaften</h4>
                <div className="p-3 bg-noc-dark rounded-md border border-noc-border">
                    <DetailRenderer data={element.properties} />
                </div>
            </div>
        );
    };

    export default DetailsTab;
    """),    ('frontend/src/components/topology/tabs/ActionsTab.jsx', """
    import React from 'react';

    const ActionButton = ({ label, onClick, color = 'noc-blue', disabled = false }) => (
      <button
        onClick={onClick}
        disabled={disabled}
        className={`w-full text-left px-4 py-2 mt-2 text-white rounded-md bg-${color} hover:bg-opacity-80 transition-all disabled:bg-noc-border disabled:text-noc-text-secondary disabled:cursor-not-allowed`}
      >
        {label}
      </button>
    );

    const ActionsTab = ({ element }) => {
        const handleAction = async (actionType, payload = {}) => {
            const token = localStorage.getItem('ultranoc_token');
            try {
                await fetch(`/api/v1/simulation/devices/${element.properties.id}/action`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                    body: JSON.stringify({ type: actionType, payload }),
                });
            } catch (error) {
                console.error(`Fehler bei Aktion ${actionType}:`, error);
            }
        };

        const renderActions = () => {
            const { type, status } = element.properties;
            switch (type) {
                case 'Core Router':
                case 'OLT':
                case 'ONT':
                    return <>
                        <ActionButton label="Gerät neustarten" onClick={() => handleAction('reboot')} color="noc-yellow" disabled={status === 'rebooting'} />
                        <ActionButton label="Status auf 'offline' setzen" onClick={() => handleAction('set_status', { status: 'offline' })} color="noc-red" disabled={status === 'offline'} />
                        <ActionButton label="Status auf 'online' setzen" onClick={() => handleAction('set_status', { status: 'online' })} color="noc-green" disabled={status === 'online'}/>
                    </>;
                case 'Muffe':
                    return <ActionButton label="Außendiensteinsatz anfordern" onClick={() => handleAction('request_field_service')} disabled={status === 'maintenance'} />;
                default:
                    return <p className="text-noc-text-secondary">Für dieses Element sind keine Aktionen verfügbar.</p>;
            }
        };

        return (
            <div>
                <h3 className="text-md font-bold text-noc-text mb-4">Verfügbare Aktionen</h3>
                {renderActions()}
            </div>
        );
    };

    export default ActionsTab;
    """),    ('frontend/src/components/topology/tabs/TerminalTab.jsx', """
    import React, { useState, useEffect, useRef } from 'react';

    const TerminalTab = ({ element }) => {
        const [output, setOutput] = useState([]);
        const [input, setInput] = useState('');
        const [history, setHistory] = useState([]);
        const [historyIndex, setHistoryIndex] = useState(-1);
        const endOfMessagesRef = useRef(null);
        const inputRef = useRef(null);
        const [isFetching, setIsFetching] = useState(false);

        const scrollToBottom = () => endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });

        useEffect(scrollToBottom, [output]);

        useEffect(() => {
            setOutput([`Verbunden mit ${element.properties.label} (${element.properties.id}).`]);
            setInput('');
            setHistory([]);
            setHistoryIndex(-1);
            inputRef.current?.focus();
        }, [element.properties.id]);

        const handleCommand = async (e) => {
            if (e.key === 'Enter' && input.trim() !== '' && !isFetching) {
                const command = input.trim();
                if (command) setHistory(prev => [command, ...prev]);
                setHistoryIndex(-1);
                
                const prompt = `<span class="text-noc-green">${element.properties.label}></span> ${command}`;
                setOutput(prev => [...prev, prompt]);
                setInput('');
                setIsFetching(true);

                const token = localStorage.getItem('ultranoc_token');
                try {
                    const response = await fetch(`/api/v1/simulation/devices/${element.properties.id}/action`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                        body: JSON.stringify({ type: 'get_cli_output', payload: { command } }),
                    });
                    const data = await response.json();
                    setOutput(prev => [...prev, data.output.replace(/\\n/g, '<br/>')]);
                } catch (error) {
                    setOutput(prev => [...prev, `<span class="text-noc-red">Fehler bei der Befehlsausführung.</span>`]);
                } finally {
                    setIsFetching(false);
                }
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                if (history.length > 0) {
                    const newIndex = Math.min(history.length - 1, historyIndex + 1);
                    setHistoryIndex(newIndex);
                    setInput(history[newIndex] || '');
                }
            } else if (e.key === 'ArrowDown') {
                e.preventDefault();
                if (historyIndex > 0) {
                    const newIndex = historyIndex - 1;
                    setHistoryIndex(newIndex);
                    setInput(history[newIndex] || '');
                } else {
                    setHistoryIndex(-1);
                    setInput('');
                }
            }
        };

        useEffect(() => {
            if (!isFetching) {
                inputRef.current?.focus();
            }
        }, [isFetching]);

        return (
            <div className="h-full flex flex-col font-mono text-sm">
                <div className="flex-grow bg-noc-dark p-2 rounded-t-md overflow-y-auto whitespace-pre-wrap border border-noc-border" onClick={() => inputRef.current?.focus()}>
                    {output.map((line, index) => <div key={index} dangerouslySetInnerHTML={{ __html: line }} />)}
                    <div ref={endOfMessagesRef} />
                </div>
                <div className="flex bg-noc-dark p-2 rounded-b-md border-x border-b border-noc-border">
                    <span className="text-noc-green">{element.properties.label}></span>
                    <input
                        ref={inputRef}
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleCommand}
                        className="bg-transparent border-none outline-none text-noc-text flex-grow ml-2"
                        disabled={isFetching}
                        autoFocus
                    />
                </div>
            </div>
        );
    };

    export default TerminalTab;
    """),    ('frontend/src/components/incidents/IncidentGraph.jsx', """
    import React from 'react';

    const IncidentGraph = ({ incident }) => {
      // Dies ist eine statische Darstellung des Graphen aus dem Bild.
      // Eine dynamische Version würde eine Graphen-Bibliothek (D3, VisX)
      // und eine Layout-Engine benötigen, um die Knoten und Kanten basierend
      // auf den `incident.events`-Daten zu positionieren.
      const nodes = {
          '04': { x: '15%', y: '25%', label: 'Host-base firewall blocked' },
          '06': { x: '20%', y: '70%', label: 'Failed SSH login' },
          '03': { x: '40%', y: '15%', label: 'Successful SSH login' },
          '38': { x: '45%', y: '45%', label: 'Failed SSH login' },
          '14': { x: '50%', y: '75%', label: 'Failed network login' },
          '29': { x: '60%', y: '90%', label: 'Failed network login' },
          '09': { x: '65%', y: '10%', label: 'Failed SSH login' },
          '22': { x: '70%', y: '55%', label: 'Host-base firewall blocked' },
          '13': { x: '80%', y: '25%', label: 'Account logged out' },
          '07': { x: '90%', y: '10%', label: 'Failed network login' },
      };
      
      const links = [
          ['04', '06'], ['04', '03'], ['06', '14'], ['03', '09'], ['03', '38'],
          ['38', '14'], ['38', '22'], ['14', '29'], ['09', '07'], ['09', '13'],
          ['22', '13'], ['22', '09']
      ];

      return (
        <div className="w-full h-full bg-noc-light-dark rounded-lg border border-noc-border p-6 relative overflow-hidden">
          <h2 className="text-xl font-bold text-noc-text">{incident.title}</h2>
          <span className="text-sm bg-noc-red text-white px-2 py-1 rounded-full absolute top-6 right-6">Malicious</span>
          
          <div className="mt-10 relative h-full">
            <svg className="absolute inset-0 w-full h-full">
                <defs>
                    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#30363d" />
                    </marker>
                </defs>
                {links.map(([source, target], i) => (
                    <line key={i} x1={nodes[source].x} y1={nodes[source].y} x2={nodes[target].x} y2={nodes[target].y} stroke="#30363d" markerEnd="url(#arrow)" />
                ))}
            </svg>
            
            {Object.entries(nodes).map(([id, {x, y, label}]) => (
                <div key={id} className="absolute" style={{ left: x, top: y, transform: 'translate(-50%, -50%)' }}>
                    <div className="w-12 h-12 rounded-full border-2 border-noc-blue/50 bg-noc-dark flex items-center justify-center font-bold text-noc-blue text-lg">
                        <div className="w-10 h-10 rounded-full border-2 border-noc-blue/80 bg-noc-dark/50 flex items-center justify-center">{id}</div>
                    </div>
                    <div className="text-center text-xs mt-2 w-24 text-noc-text-secondary">{label}</div>
                </div>
            ))}
          </div>
        </div>
      );
    };
    export default IncidentGraph;
    """),    ('frontend/src/components/incidents/SocPanel.jsx', """
    import React, { useState } from 'react';
    import { ShieldCheck, UserCheck, AlertOctagon, Files, ShieldOff, MessageSquare } from 'lucide-react';

    const StatItem = ({ icon, label, value }) => (
        <div>
            <div className="text-xs text-noc-text-secondary flex items-center gap-2">{icon}{label}</div>
            <div className="text-lg font-bold text-noc-text">{value}</div>
        </div>
    );

    const SocPanel = ({ incident }) => {
      const [llmAnalysis, setLlmAnalysis] = useState('');
      const [isAnalyzing, setIsAnalyzing] = useState(false);
      // In einer echten App würde der Verlauf hier aus einem Context oder State kommen
      // const [llmHistory, setLlmHistory] = useState([]); 

      const handleLlmRequest = async (type) => {
        setIsAnalyzing(true);
        setLlmAnalysis('Analysiere...');
        
        // Hier würde der API-Aufruf an das Backend erfolgen,
        // das dann mit dem LLM kommuniziert.
        // const response = await fetch('/api/v1/llm/analyze', { ... });
        
        // Simulierte Antwort für die Demo
        const simulatedResponse = type === 'root_cause' 
          ? "Root Cause: Wahrscheinlich ein erfolgreicher Brute-Force-Angriff, der zu einem Credential-Diebstahl führte, gefolgt von lateralen Bewegungen."
          : "Mitigations: 1. Betroffenen Host sofort aus dem Netzwerk isolieren. 2. Alle Passwörter des kompromittierten Users zurücksetzen. 3. SSH-Logs auf weitere verdächtige Aktivitäten prüfen.";
        
        setTimeout(() => {
            setLlmAnalysis(simulatedResponse);
            // setLlmHistory(prev => [...prev, {role: 'user', content: prompt}, {role: 'assistant', content: simulatedResponse}]);
            setIsAnalyzing(false);
        }, 1500);
      };

      return (
        <div className="bg-noc-light-dark rounded-lg border border-noc-border h-full flex flex-col p-6 text-noc-text">
            <div>
                <h3 className="text-lg font-bold">Overview</h3>
                <p className="text-sm text-noc-text-secondary mt-2">{incident.summary}</p>
            </div>
          
            <div className="grid grid-cols-2 gap-y-4 gap-x-2 mt-6">
                <StatItem icon={<AlertOctagon size={14}/>} label="Events" value={incident.metrics.events} />
                <StatItem icon={<UserCheck size={14}/>} label="Assignee" value={incident.assignee} />
                <StatItem icon={<ShieldOff size={14}/>} label="Attackers" value={incident.metrics.attackers} />
                <StatItem icon={<Files size={14}/>} label="Artifacts" value={incident.metrics.artifacts} />
            </div>
          
            <div className="mt-6 border-t border-noc-border pt-4">
                <h4 className="text-md font-bold text-noc-text-secondary">SOC-Analyst (LLM-Powered)</h4>
                <div className="flex gap-2 mt-2">
                    <button onClick={() => handleLlmRequest('root_cause')} disabled={isAnalyzing} className="text-xs bg-noc-border py-1 px-2 rounded hover:bg-noc-blue disabled:opacity-50">Suggest Root Cause</button>
                    <button onClick={() => handleLlmRequest('mitigation')} disabled={isAnalyzing} className="text-xs bg-noc-border py-1 px-2 rounded hover:bg-noc-green disabled:opacity-50">Recommend Mitigations</button>
                </div>
                {llmAnalysis && (
                    <div className="mt-2 p-3 bg-noc-dark rounded text-xs text-noc-text-secondary border border-noc-border">
                        {llmAnalysis}
                    </div>
                )}
            </div>

            <div className="mt-auto pt-6 flex gap-4">
                <button className="flex-1 bg-noc-border text-noc-text-secondary py-2 rounded-md hover:opacity-80">Found a mistake</button>
                <button className="flex-1 bg-noc-blue text-white py-2 rounded-md hover:opacity-80">Change status</button>
            </div>
        </div>
      );
    };
    export default SocPanel;
    """),# =======================================================================
# PART 15: FRONTEND - SANDBOX & UI (TEIL 1/11)
# =======================================================================
    ('frontend/src/components/sandbox/SandboxControlPanel.jsx', """
    import React, { useState, useContext, useEffect } from 'react';
    import { TopologyContext } from '../../contexts/TopologyContext';
    import { MapPin, Router, Link, GitPullRequest, Save, FolderOpen, Plus, Settings } from 'lucide-react';
    
    // Eine einfache Gerätedatenbank für den Sandbox-Modus
    const deviceTemplates = [
        { id: 'new-router', label: 'Neuer Router', type: 'Core Router', details: { ip_address: '0.0.0.0', firmware: { os: 'Generic OS', version: '1.0' }}},
        { id: 'new-olt', label: 'Neue OLT', type: 'OLT', details: { active_onts: 0 }},
        { id: 'new-muffe', label: 'Neue Muffe', type: 'Muffe', details: { fiber_type: 'SMF' }},
        { id: 'new-ont', label: 'Neues ONT', type: 'ONT', details: { rx_power_dbm: -25.0 }}
    ];

    const SandboxControlPanel = () => {
        const { topology, setTopology } = useContext(TopologyContext);
        const [mode, setMode] = useState('view'); // 'view', 'addNode', 'addLink'
        const [selectedNodeType, setSelectedNodeType] = useState(deviceTemplates[0].id);
        const [selectedLinkSource, setSelectedLinkSource] = useState(null);

        const handleAddNode = () => {
            setMode('addNode');
            alert('Klicken Sie auf die Karte, um einen neuen Knoten zu platzieren.');
        };

        const handleMapClick = (e) => {
            if (mode === 'addNode') {
                const newId = `node-${Date.now()}`;
                const newDeviceTemplate = deviceTemplates.find(t => t.id === selectedNodeType);
                const newNode = {
                    type: "Feature",
                    geometry: { type: "Point", coordinates: [e.latlng.lng, e.latlng.lat] },
                    properties: { 
                        id: newId, 
                        label: newDeviceTemplate.label, 
                        type: newDeviceTemplate.type, 
                        status: 'online', 
                        details: newDeviceTemplate.details 
                    }
                };
                setTopology(prev => ({
                    ...prev,
                    features: [...prev.features, newNode]
                }));
                setMode('view');
            } else if (mode === 'addLink' && selectedLinkSource) {
                // Implement link creation logic in ControlPanel or directly in MapView
                // For now, this is handled via an interaction in MapView
                setSelectedLinkSource(null); // Reset after potential link creation attempt
            }
        };

        const handleAddLink = () => {
            setMode('addLink');
            setSelectedLinkSource(null);
            alert('Klicken Sie auf den ersten Knoten für die Verbindung.');
        };

        const handleNodeClickForLink = (nodeId) => {
            if (mode === 'addLink') {
                if (!selectedLinkSource) {
                    setSelectedLinkSource(nodeId);
                    alert(`Erster Knoten ausgewählt: ${nodeId}. Klicken Sie auf den zweiten Knoten.`);
                } else {
                    const newLink = {
                        type: "Feature",
                        geometry: { type: "LineString", coordinates: [] }, // Koordinaten werden vom MapView gesetzt
                        properties: {
                            source: selectedLinkSource,
                            target: nodeId,
                            status: 'online',
                            type: 'Fiber Link',
                            length_km: 1.0, // Standardwert, später editierbar
                        }
                    };
                    setTopology(prev => ({
                        ...prev,
                        features: [...prev.features, newLink]
                    }));
                    setMode('view');
                    setSelectedLinkSource(null);
                }
            }
        };

        return (
            <div className="bg-noc-light-dark text-noc-text rounded-lg border border-noc-border p-4 h-full flex flex-col space-y-4">
                <h3 className="text-xl font-bold mb-4">Sandbox Steuerung</h3>
                
                {/* Modus-Auswahl */}
                <div className="grid grid-cols-2 gap-2">
                    <button 
                        onClick={handleAddNode} 
                        className={`flex items-center justify-center gap-2 py-2 px-3 rounded-md text-sm font-medium transition-colors ${mode === 'addNode' ? 'bg-noc-blue text-white' : 'bg-noc-border hover:bg-noc-blue hover:text-white'}`}
                    >
                        <Plus size={16}/> Knoten hinzufügen
                    </button>
                    <button 
                        onClick={handleAddLink} 
                        className={`flex items-center justify-center gap-2 py-2 px-3 rounded-md text-sm font-medium transition-colors ${mode === 'addLink' ? 'bg-noc-blue text-white' : 'bg-noc-border hover:bg-noc-blue hover:text-white'}`}
                    >
                        <GitPullRequest size={16}/> Link zeichnen
                    </button>
                </div>

                {mode === 'addNode' && (
                    <div className="mt-2">
                        <label className="block text-sm text-noc-text-secondary mb-1">Gerätetyp:</label>
                        <select 
                            value={selectedNodeType} 
                            onChange={(e) => setSelectedNodeType(e.target.value)}
                            className="w-full p-2 bg-noc-dark border border-noc-border rounded-md text-noc-text"
                        >
                            {deviceTemplates.map(template => (
                                <option key={template.id} value={template.id}>{template.label}</option>
                            ))}
                        </select>
                    </div>
                )}
                
                {/* Separator */}
                <div className="border-t border-noc-border pt-4 mt-4"></div>

                {/* Allgemeine Aktionen */}
                <div className="flex flex-col space-y-2">
                    <button className="flex items-center gap-2 py-2 px-3 rounded-md text-sm font-medium bg-noc-green hover:bg-opacity-80 text-white">
                        <Save size={16}/> Topologie Speichern
                    </button>
                    <button className="flex items-center gap-2 py-2 px-3 rounded-md text-sm font-medium bg-noc-blue hover:bg-opacity-80 text-white">
                        <FolderOpen size={16}/> Topologie Laden
                    </button>
                    <button className="flex items-center gap-2 py-2 px-3 rounded-md text-sm font-medium bg-noc-purple hover:bg-opacity-80 text-white">
                        <Settings size={16}/> Szenario Editor
                    </button>
                </div>
            </div>
        );
    };

    export default SandboxControlPanel;
    """),# =======================================================================
# PART 15: FRONTEND - SANDBOX & UI (TEIL 2/11)
# =======================================================================
    ('frontend/src/components/sandbox/DevicePropertiesPanel.jsx', """
    import React, { useState, useEffect, useContext } from 'react';
    import { TopologyContext } from '../../contexts/TopologyContext';
    import { X } from 'lucide-react';

    const DevicePropertiesPanel = ({ device, onClose }) => {
        const { setTopology } = useContext(TopologyContext);
        const [properties, setProperties] = useState(device.properties);
        const [geometry, setGeometry] = useState(device.geometry);

        useEffect(() => {
            setProperties(device.properties);
            setGeometry(device.geometry);
        }, [device]);

        const handleChange = (e) => {
            const { name, value, type, checked } = e.target;
            if (name.startsWith('details.')) {
                const detailKey = name.split('.')[1];
                setProperties(prev => ({
                    ...prev,
                    details: {
                        ...prev.details,
                        [detailKey]: value
                    }
                }));
            } else {
                setProperties(prev => ({
                    ...prev,
                    [name]: type === 'checkbox' ? checked : value
                }));
            }
        };

        const handleSave = () => {
            setTopology(prev => ({
                ...prev,
                features: prev.features.map(f => 
                    f.properties.id === device.properties.id 
                    ? { ...f, properties: properties, geometry: geometry } 
                    : f
                )
            }));
            onClose(); // Schließt das Panel nach dem Speichern
        };

        const renderPropertyInput = (key, value, path = '') => {
            const name = path ? `${path}.${key}` : key;
            if (typeof value === 'boolean') {
                return (
                    <input 
                        type="checkbox" 
                        name={name} 
                        checked={value} 
                        onChange={handleChange} 
                        className="ml-2"
                    />
                );
            }
            if (typeof value === 'number') {
                return (
                    <input 
                        type="number" 
                        name={name} 
                        value={value} 
                        onChange={handleChange} 
                        className="w-full p-1 bg-noc-dark border border-noc-border rounded-md text-noc-text text-sm"
                        step="any"
                    />
                );
            }
            if (typeof value === 'string' && (key.includes('ip_address') || key.includes('firmware'))) {
                 return (
                    <input 
                        type="text" 
                        name={name} 
                        value={value} 
                        onChange={handleChange} 
                        className="w-full p-1 bg-noc-dark border border-noc-border rounded-md text-noc-text text-sm"
                    />
                );
            }
            // Für komplexe Objekte rekursiv rendern
            if (typeof value === 'object' && value !== null) {
                if (Array.isArray(value)) {
                    return (
                        <div className="pl-2 border-l border-noc-border ml-2">
                            {value.map((item, idx) => (
                                <div key={idx} className="mt-1">
                                    <span className="text-noc-text-secondary">{idx}: </span>
                                    {renderPropertyInput(idx, item, `${name}`)}
                                </div>
                            ))}
                        </div>
                    );
                }
                return (
                    <div className="pl-2 border-l border-noc-border ml-2">
                        {Object.entries(value).map(([subKey, subValue]) => (
                            <div key={subKey} className="mt-1">
                                <span className="text-noc-text-secondary">{subKey}: </span>
                                {renderPropertyInput(subKey, subValue, `${name}`)}
                            </div>
                        ))}
                    </div>
                );
            }
            return (
                <input 
                    type="text" 
                    name={name} 
                    value={value} 
                    onChange={handleChange} 
                    className="w-full p-1 bg-noc-dark border border-noc-border rounded-md text-noc-text text-sm"
                />
            );
        };

        return (
            <div className="bg-noc-light-dark text-noc-text rounded-lg border border-noc-border p-4 h-full flex flex-col">
                <div className="flex justify-between items-center border-b border-noc-border pb-3 mb-3">
                    <h3 className="text-lg font-bold">Eigenschaften von {properties.label}</h3>
                    <button onClick={onClose} className="text-noc-text-secondary hover:text-white p-1 rounded-full hover:bg-noc-border">
                        <X size={16} />
                    </button>
                </div>
                
                <div className="flex-grow overflow-y-auto space-y-2 text-sm">
                    {Object.entries(properties).map(([key, value]) => (
                        <div key={key} className="flex items-center">
                            <label className="w-1/3 text-noc-text-secondary pr-2 truncate">{key}:</label>
                            <div className="w-2/3">
                                {renderPropertyInput(key, value)}
                            </div>
                        </div>
                    ))}
                </div>

                <button 
                    onClick={handleSave} 
                    className="mt-4 py-2 px-4 bg-noc-blue text-white font-semibold rounded-md hover:bg-opacity-80"
                >
                    Änderungen speichern
                </button>
            </div>
        );
    };

    export default DevicePropertiesPanel;
    """),    ('frontend/src/components/Map/LeafletMap.jsx', """
    import React, { useState, useEffect, useCallback, useContext } from 'react';
    import { MapContainer, TileLayer, Marker, Polyline, useMapEvents, useMap } from 'react-leaflet';
    import L from 'leaflet';
    import 'leaflet/dist/leaflet.css';
    import { TopologyContext } from '../../contexts/TopologyContext';
    import DevicePropertiesPanel from '../sandbox/DevicePropertiesPanel';

    // Leaflet Icon Fix (Vite)
    delete L.Icon.Default.prototype._getIconUrl;
    L.Icon.Default.mergeOptions({
        iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
        iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
        shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
    });

    const getStatusColor = (status) => {
        switch (status) {
            case 'online': return '#3fb950';
            case 'offline': return '#f85149';
            case 'rebooting':
            case 'updating':
            case 'maintenance':
            case 'warning': return '#d29922';
            default: return '#8b949e';
        }
    };

    const LeafletMap = () => {
        const { topology, selectElement, clearSelection, tracedPath, mapBounds, setTopology } = useContext(TopologyContext);
        const [isAddingLink, setIsAddingLink] = useState(false);
        const [newLinkSource, setNewLinkSource] = useState(null);
        const [selectedForLink, setSelectedForLink] = useState(null);
        const [showProperties, setShowProperties] = useState(false);

        const handleMapClick = (e) => {
            if (isAddingLink) {
                if (selectedForLink) {
                    // Erstelle neuen Link im Zustand
                    setTopology(prev => {
                        const newLink = {
                            type: "Feature",
                            geometry: { type: "LineString", coordinates: [ [selectedForLink.geometry.coordinates[0], selectedForLink.geometry.coordinates[1]], [e.latlng.lng, e.latlng.lat] ] },
                            properties: {
                                source: selectedForLink.properties.id,
                                target: `new-node-${Date.now()}`,
                                status: 'online',
                                type: 'Fiber Link',
                                length_km: 1.0,
                            }
                        };
                        return { ...prev, features: [...prev.features, newLink] };
                    });
                    setIsAddingLink(false);
                    setSelectedForLink(null);
                }
                else {
                    alert("Bitte wähle zuerst einen Startknoten aus.");
                }
            }
        };

        const handleNodeClick = (feature) => {
            if(isAddingLink) {
                setSelectedForLink(feature);
                alert("Knoten für Verbindung ausgewählt. Klicken Sie auf einen zweiten Knoten.")
            } else {
                selectElement(feature);
                setShowProperties(true);
            }
        };

        const handleCloseProperties = () => {
            setShowProperties(false);
            clearSelection();
        };
        
        const styleFeature = (feature) => {
            const isSelected = selectedElement?.properties?.id === feature.properties.id;
            const isLinkSelected = selectedElement?.properties?.source === feature.properties.source && selectedElement?.properties?.target === feature.properties.target;
            const inPath = tracedPath && (
                (feature.properties.id && tracedPath.includes(feature.properties.id)) || 
                (feature.properties.source && tracedPath.includes(feature.properties.source) && tracedPath.includes(feature.properties.target))
            );

            const baseStyle = getStatusColor(feature.properties.status);
            let style = { color: baseStyle, weight: 3, opacity: 0.9, fillOpacity: 0.8, fillColor: baseStyle, dashArray: null };

            if (isSelected || isLinkSelected) {
                style.weight = 5;
                style.color = '#58a6ff';
            }
            if (inPath) {
                style.weight = 5;
                style.color = '#a371f7';
                style.dashArray = '10, 5';
            }
            return style;
        };
        
        const pointToLayer = (feature, latlng) => {
             return L.circleMarker(latlng, {
                ...styleFeature(feature),
                radius: 8,
             });
        };

        const AddLinkControl = () => {
            const map = useMap();
            useEffect(() => {
                if (isAddingLink) {
                    map.getContainer().style.cursor = 'crosshair';
                } else {
                    map.getContainer().style.cursor = '';
                }
                return () => {
                    map.getContainer().style.cursor = '';
                };
            }, [map, isAddingLink]);
            return null;
        };

        const MapEvents = () => {
            useMapEvents({
                click: handleMapClick
            });
            return null;
        };

        return (
            <div className="flex h-full w-full">
                <div className="flex-grow h-full relative">
                    <MapContainer center={[51.9607, 7.6261]} zoom={13} style={{ height: '60vh', width: '100%' }}>
                        <TileLayer
                            attribution='© <a href="https://carto.com/attributions">CARTO</a>'
                            url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                        />
                        {topology.features && topology.features.map((feature, index) => (
                            feature.geometry.type === "Point" ? (
                                <Marker
                                    key={index}
                                    position={[feature.geometry.coordinates[1], feature.geometry.coordinates[0]]}
                                    icon={L.divIcon({ className: 'custom-icon', html: `<span style="color:${getStatusColor(feature.properties.status)}">●</span>` })}
                                    eventHandlers={{ click: () => handleNodeClick(feature) }}
                                />
                            ) : (
                                <Polyline
                                    key={index}
                                    positions={[
                                        [feature.geometry.coordinates[0][1], feature.geometry.coordinates[0][0]],
                                        [feature.geometry.coordinates[1][1], feature.geometry.coordinates[1][0]]
                                    ]}
                                    style={styleFeature(feature)}
                                />
                            )
                        ))}
                        <MapEvents />
                        <AddLinkControl/>
                    </MapContainer>
                </div>
                {selectedElement && showProperties && (
                    <div className="w-96 h-full flex-shrink-0">
                        <DevicePropertiesPanel device={selectedElement} onClose={handleCloseProperties} />
                    </div>
                )}
            </div>
        );
    };

    export default LeafletMap;
    """),    ('frontend/src/components/UI/Button.jsx', """
    import React from 'react';
    const Button = ({ label, onClick }) => <button onClick={onClick}>{label}</button>;
    export default Button;
    """),    ('frontend/src/components/UI/Card.jsx', """
    import React from 'react';
    const Card = ({ children }) => <div className="card">{children}</div>;
    export default Card;
    """),    ('frontend/src/components/UI/Modal.jsx', """
    import React from 'react';
    const Modal = ({ isOpen, children }) => isOpen ? <div className="modal">{children}</div> : null;
    export default Modal;
    """),    ('frontend/src/components/UI/StatusIndicator.jsx', """
    import React from 'react';
    const StatusIndicator = ({ status }) => <span className={`status ${status}`}></span>;
    export default StatusIndicator;
    """),    ('frontend/src/api/apiClient.js', """
    export const fetchData = async (endpoint) => (await fetch(endpoint)).json();
    """),    ('frontend/src/data/incident_example.json', """
    {
      "id": 1,
      "title": "Credential dumping via MimiKats",
      "summary": "Professionally grow e-business web-readiness rather than technically sound metrics. Phosfluorescently foster high standards in schemas for business value.",
      "status": "Pending",
      "assignee": "Cole Bishop",
      "metrics": {
        "events": 195,
        "attackers": "01",
        "victims": "02",
        "artifacts": 23,
        "mitigations": "07",
        "notes": "03"
      },
      "events": [
        { "id": "03", "description": "Successfull SSH login", "time": "18:10" },
        { "id": "04", "description": "Host-base firewall blocked", "time": "14:30" },
        { "id": "09", "description": "Failed SSH login", "time": "18:20" }
      ]
    }
    """),    ('frontend/src/data/devices.js', """
    const devices = [
        {
            "id": 1,
            "name": "Router Alpha",
            "type": "Router",
            "ip": "10.0.0.1",
            "vlan": 1,
            "cpu_load": 10,
            "mem_load": 20,
            "status": "online",
            "lat": 52.5200,
            "lon": 13.4050,
            "connected_to": [2, 3],
            "redundancy_group": 1
        },
        {
            "id": 2,
            "name": "Switch Beta",
            "type": "Switch",
            "ip": "10.0.0.2",
            "vlan": 1,
            "cpu_load": 15,
            "mem_load": 25,
            "status": "online",
            "lat": 52.5205,
            "lon": 13.4060,
            "connected_to": [1, 4]
        },
        {
            "id": 3,
            "name": "Firewall Gamma",
            "type": "Firewall",
            "ip": "10.0.1.1",
            vlan: 2,
            cpu_load: 30,
            mem_load: 40,
            status: "online",
            lat: 52.5210,
            lon: 13.4070,
            connected_to: [1]
        },
        {
            "id": 4,
            "name": "Server Delta",
            "type": "Server",
            "ip": "10.0.1.2",
            vlan: 2,
            cpu_load: 50,
            mem_load: 60,
            status: "online",
            lat: 52.5215,
            lon: 13.4080,
            connected_to: [2]
        },
    ];

    export default devices;
    """,),
]

def create_project_structure():
    """
    Erstellt die gesamte Verzeichnisstruktur und schreibt alle
    definierten Dateien basierend auf der `PROJECT_FILES`-Liste.
    """
    project_root = os.getcwd()
    print("Starte die Erstellung des UltraNOC-Projekts im Verzeichnis:")
    print(f"-> {project_root}\\n")
    
    total_files = len(PROJECT_FILES)
    if total_files == 0:
        print("\\nWARNUNG: Die 'PROJECT_FILES'-Liste ist leer.")
        print("Bitte fügen Sie die Code-Module aus den nächsten Nachrichten ein.")
        return

    total_bytes_written = 0
    for index, (file_path, file_content) in enumerate(PROJECT_FILES):
        # Erstelle das Verzeichnis, falls es nicht existiert
        full_path = os.path.join(project_root, file_path)
        directory = os.path.dirname(full_path)
        if directory and not os.path.exists(directory):
            print(f"-> Erstelle Verzeichnis: {directory}")
            os.makedirs(directory)
            
        # Schreibe den Inhalt in die Datei
        try:
            content_to_write = textwrap.dedent(file_content).strip()
            byte_count = len(content_to_write.encode('utf-8'))
            total_bytes_written += byte_count

            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content_to_write)
            
            progress = f"[{index + 1}/{total_files}]"
            print(f"{progress:>10} Schreibe Datei:      {file_path:<60} ({byte_count} Bytes)")

        except Exception as e:
            print(f"!!! FEHLER beim Schreiben von {file_path}: {e}")
            return
            
    print("\\n" + "="*70)
    print("✅ Projekt 'UltraNOC' wurde erfolgreich auf Ihrer Festplatte erstellt!")
    print(f"   - {total_files} Dateien geschrieben.")
    print(f"   - Gesamtgröße des generierten Codes: {total_bytes_written / 1024:.2f} KB")
    print("="*70)
    print("\\nNÄCHSTE SCHRITTE:")
    print("1. Stellen Sie sicher, dass Docker und Docker Compose installiert sind.")
    print("2. Öffnen Sie ein Terminal im Hauptverzeichnis dieses Projekts.")
    print("3. Führen Sie 'docker-compose up --build' aus, um alle Dienste zu starten.")
    print("   (Der erste Build kann einige Minuten dauern.)")
    print("4. Warten Sie, bis die Container laufen, und führen Sie dann in einem ZWEITEN Terminal aus:")
    print("   'docker-compose exec backend python initial_setup.py'")
    print("5. Öffnen Sie Ihren Browser und gehen Sie zu http://localhost:5173")
    print("\\n   Viel Spaß mit UltraNOC! (Login: admin / admin123)")


if __name__ == "__main__":
    create_project_structure()