# UltraNOC – Änderungsdetails zu bestehenden Dateien

## Übersicht: Modifizierte Dateien (laut Git)

### 🔄 Backend

#### `backend/app/main.py`
- Eingebundene neue Router: `path_metrics`, `topology_router`, `topology_path`
- Jetzt zentrale Registrierungsstelle für alle Simulation-/Topologie-Router

#### `backend/app/routers/topology.py`
- Erweiterung für zusätzliche Pfad- und Redundanzlogik
- Übergangslösung für neue Pfad-Metrikfunktionen

#### `backend/app/simulation/cables.py`
- Aktualisierung der Fiber-Logik mit realistischen Dämpfungswerten
- Berechnung von `db_loss` anhand von Längenwerten und Kabeltypen

#### `data/topology/core_topology.json`
- Realistische Netzstruktur: Düsseldorf → Kleve → Wesel → Bocholt (+ Rees/Haldern)
- Geräte pro Ortstyp: Core, BNG, OLT, ONT, CPE
- Koordinaten für Kartenansicht (Leaflet-kompatibel)

#### `docs/devices/huawei_ma5800x17.md`
- Ergänzt: Ports, typische Topologieposition (z. B. Access-OLT)
- Basis für CLI-Interaktion im späteren Modul

---

### 🎨 Frontend

#### `frontend/src/App.jsx`
- Routingstruktur erweitert für neue Pfade wie `/topology`
- Einbindung `Layout.jsx`, geschützte Bereiche mit `ProtectedRoute`

#### `frontend/src/components/layout/Layout.jsx`
- Enthält Sidebar, Header und `Outlet` (Hauptinhalt)
- Import-Fixes wegen Groß-/Kleinschreibung von `Sidebar`

#### `frontend/src/components/layout/LogoutButton.jsx`
- Einbindung von `AuthContext`
- Abmelden via Token-Reset und Navigation

#### `frontend/src/components/layout/Sidebar.jsx`
- Navigationseinträge aktualisiert (Metriken, Topologie, Alarme etc.)
- Aktiver Link visuell hervorgehoben (Tailwind)

#### `frontend/src/contexts/AuthContext.jsx`
- Doppelt importiertes `React` entfernt (Fehlerbehebung)
- Token-Handling & Navigation `useNavigate` fixiert

#### `frontend/src/layout/MainLayout.jsx`
- Verwaltet Auth-Gate für alle Routen
- Legacy-Ersatz durch `Layout.jsx`

#### `frontend/src/routes/AppRouter.jsx`
- Routinganpassung für `TopologyView`, Dashboard etc.
- Login-Route explizit geschützt

#### `frontend/vite.config.js`
- Server-Konfiguration für Aliases (`@/components`, `@/services`)
- Unterstützung für statische Assets (`leaflet`, `favicon.ico`)

---

## 🧹 Entfernte Datei

#### `frontend/src/components/AlarmPanel.jsx`
- Veraltet, wurde durch `Widgets/AlarmPanel.jsx` ersetzt
