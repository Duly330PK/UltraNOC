up-Pfade, gestrichelt)

CableInfoPanel (Details bei Link-Klick)

PathMetricsPanel (Verzögerung, Loss, etc.)

PathPanel (konkreter Pfad von Gerät A → B)

MetricsPanel / AlarmPanel (Mock-Widgets)

🔄 State Hooks
js
Copy
Edit
const { devices } = useTopologyData();
const path = usePathData(selectedDevice?.id);
const pathMetrics = usePathMetrics(selectedDevice?.id);
🧰 Backend – FastAPI + SQLAlchemy
🔹 Struktur
python
Copy
Edit
/app
├── main.py              # App-Facade, API Router-Mounting
├── routers/
│   ├── topology.py      # Geräte- und Linkdaten
│   ├── path_metrics.py  # Simulierte Pfadmetriken (delay, loss, jitter)
│   ├── simulation_control.py # Simulationsstatus togglebar
├── simulation/
│   ├── cables.py        # Kabelphysik (dB, Dämpfung etc.)
│   ├── redundancy.py    # Dijkstra + alternative Pfade
🔹 Beispiel-Router: path_metrics.py
python
Copy
Edit
@router.get("/path/metrics/{source_id}/{target_id}")
async def get_path_metrics(source_id: str, target_id: str):
    return {
        "path": [
            {"from": "core", "to": "bng", "delay_ms": 3.2, ...}
        ]
    }
🔹 Redundanz
redundancy.py:

Eingabe: Topologie-Graph

Ausgabe: Primär-/Backup-Pfad als JSON

Logik: BFS mit Knoten-Blacklisting bei Pfadwechsel

🧪 Auth / Token / Context
Frontend:
Login via AuthContext.jsx

localStorage Token persistiert

Context verfügbar über useContext(AuthContext)

Backend:
Login via /auth/token

auth_router.py + token_handler.py regeln OAuth2 + Passworthash

Tokens: JWT via python-jose

🗺️ Topologie-Engine
🔹 Basis: core_topology.json
json
Copy
Edit
{
  "nodes": [
    { "id": "core1", "type": "core", "lat": 51.2, "lon": 6.8 }
  ],
  "links": [
    { "from": "core1", "to": "bng1", "length": 43000, "fiber": "SMF" }
  ]
}
🔹 Backend-Pfade:
/api/topology/ → Geräte

/api/topology/links → Links (für Leaflet-Linien)

/api/topology/redundancy/{device_id} → logische Alternativpfade

🔄 Simulation Control (neu)
Globale Aktivierung: Simulation on/off

GET /api/simulation/status → aktiv?

POST /api/simulation/toggle → umschalten

Frontend reagiert: Zeigt nur Werte, wenn aktiv

🧱 Geräte & CLI
Noch im Ausbau (ab Update 72–75)

Geplante Features:

CLIEngine via YAML-Registry

Geräte-spezifische Prompt-Emulation

NAT-Traces und Routing-Diagnosen

Konfigurationsvergleich + Audit

📌 Technische Besonderheiten
Leaflet-Integration voll interaktiv

Modularer Hook-Ansatz: usePathData, useTopologyLinks

Geräteicons als SVG/DivIcon statt Images

Realistische Simulation von Kabeldämpfung (z. B. SMF: 0.36 dB/km)

Redundanz + Pfadmetriken komplett getrennt und optional

🧩 Erweiterbar durch
Szenario-Dateien mit Topologieänderungen

Echtzeit-Daten per WebSocket (geplant)

Drag-&-Drop Topologiemodifikation

Persistente Konfigurationen mit Snapshots

