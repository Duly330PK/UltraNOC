
# UltraNOC – Neue Dateien & Module (Update 70+)

## 🆕 Neue Backend-Dateien

### `backend/app/routers/path_metrics.py`
- Neuer API-Endpunkt: `/path/metrics/{source_id}/{target_id}`
- Liefert simulierte Delay-, Loss-, Jitter-Werte pro Pfadabschnitt
- Grundlage für spätere realistische Pfadbewertung

### `backend/app/routers/topology_path.py`, `topology_router.py`
- Getrennte Router für Pfadlogik und Topologiezugriff
- Modularer Aufbau für zukünftige Simulationen

### `backend/app/simulation/redundancy.py`
- Dijkstra-basierte Redundanzpfadberechnung
- Erkennung von Backup-Wegen und Alternativrouten
- Integration in `/api/topology/redundancy/{device_id}`

---

## 🆕 Neue Frontend-Dateien

### Leaflet-Komponenten:
- `TopologyView.jsx`: Zentrale Map-Ansicht mit Geräten, Links, Panels
- `RedundancyPathPanel.jsx`: Visualisiert Primär-/Backup-Pfade
- `CableInfoPanel.jsx`: Infobox für Leitung mit dB-Verlust, Länge etc.
- `PathPanel.jsx`: Zeigt aktuelle Routingpfade
- `PathMetricsPanel.jsx`: Darstellung von Delay/Loss/Jitter pro Hop

### Utility & Services:
- `useTopologyLinks.js`: Hook für dynamische Linkdaten
- `usePathMetrics.js`: Hook zur Metrikabfrage
- `getDeviceIcon.js`: Gerätetyp → Icon-Zuweisung

### UI-Ergänzungen:
- `AlarmPanel.jsx`, `MetricsPanel.jsx`: Widgets für Live-Meldungen & Werte
- `DWDMWidget.jsx`: Placeholder für spätere DWDM-Darstellung

---

## 🗂️ Assets / Public

### `frontend/public/leaflet/`
- Enthält `marker-icon.png`, `marker-shadow.png` für Kartenmarker

### `frontend/public/data/`
- Für spätere dynamische Topologie- oder Exportdaten

---

## 📄 Hinweise

- Alle neuen Dateien modular, eigenständig getestet
- Volle Integration in Routing, Protected Routes & Auth-System
- Datenquellen für Simulation getrennt von Darstellung

