
# UltraNOC Update-Bericht – Einstieg bis aktueller Zustand

## 📅 Beginn meiner Mitarbeit (ab Update 56)

### ✅ Update 56: Gerätemetriken & Datenbankstruktur
- Einführung der `device_metrics`-Tabelle mit `init_metrics.sql`
- FastAPI-Router `device_metrics.py` erstellt (GET-Endpunkt)
- Ziel: Echtzeit-Metriken je Gerät bereitstellen

### ✅ Update 60: Persistenter Config Store
- Implementierung von `config_store.py` mit JSON-basierter Gerätekonfigspeicherung
- Datei: `config_store.json` im Projekt verankert
- API: Konfigurationen speichern/laden via REST

### ✅ Update 64: Frontend-Grundstruktur & Login-Handling
- Layoutkomponenten (`Sidebar`, `Header`, `Layout.jsx`)
- React Context: `AuthContext.jsx` mit Tokenlogik
- `ProtectedRoute.jsx`: Zugriffskontrolle für UI-Routen

### ✅ Update 65–66: Topologie & Glasfaserintegration
- `core_topology.json` mit realistischen Geräten (OLT, ONT, CPE etc.)
- Neue Komponenten:
  - `TopologyView.jsx`: zentrale Kartenansicht (Leaflet)
  - `useTopologyLinks.js`, `CableInfoPanel.jsx`: klickbare Linien & Detail-Panel
- Geräte-Icons dynamisch generiert über `getDeviceIcon.js`

### ✅ Update 67: Redundanzpfade
- Backend: `redundancy.py`, Endpunkt `/api/topology/redundancy/{device_id}`
- Pfadberechnung mit Primär/Backup-Pfaden
- Frontend: `RedundancyPathPanel.jsx`, Darstellung auf Karte

### ✅ Update 70: Pfadmetriken
- Neue Backend-Datei: `path_metrics.py`
- Liefert simulierte Delay-, Loss-, Jitter-Werte pro Hop
- Frontend:
  - Hook: `usePathMetrics.js`
  - Anzeige: `PathMetricsPanel.jsx`
  - Integration in `TopologyView.jsx` abgeschlossen
- Fehler (z. B. `map is not a function`) durch Anpassung der API-Auswertung behoben

### 🧠 Weitere Änderungen (Dateien laut Git):
- Authentifizierung überarbeitet (`AuthContext.jsx`, `LogoutButton.jsx`)
- Sidebar-Fixes (Case Sensitivity `Layout/Sidebar.jsx`)
- Legacy-Komponenten bereinigt (`AlarmPanel.jsx` entfernt)
- Zusatzmodule für spätere 3D-Ansicht vorbereitet (`Map3DView.jsx` etc.)
- Icons & Leaflet-Ressourcen verschoben nach `public/leaflet/`

---

## 🔧 Offene Punkte
- Simulation Engine Control (Update 71) steht als nächstes an
- Szenarien-Schalter, CLI-Integration & Echtzeitrouting geplant

_Status: Projekt vollständig lauffähig mit realistischer Topologie, Routingpfaden, Metriken, Auth-UI und Kartensteuerung._
