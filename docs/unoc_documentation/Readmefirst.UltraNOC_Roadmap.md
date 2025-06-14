# UltraNOC – Technische Roadmap 2025

## Phase 1 – Grundsystem & Authentifizierung (abgeschlossen)
- Einrichtung von FastAPI-Backend mit modularem Routersystem
- Datenbankanbindung via SQLAlchemy
- Erstellung der Tabellen: `users`, `devices`, `device_metrics`, `alarms`, `routing_table`, `nat_sessions`, `vlans`, `config_snapshots`
- JWT-basierte Authentifizierung (`auth_router.py`, `token_handler.py`)
- Login-/Logout-Mechanismus via React `AuthContext`
- Geschützte Routen per `ProtectedRoute.jsx`

## Phase 2 – Geräte- und Topologieintegration
- Definition der Gerätetypen (OLT, ONT, BNG, Router, CPE etc.)
- Speicherung realistischer Gerätedaten (IP, Standort, Typ, Ports)
- Erstaufbau der `core_topology.json` mit einem vollständigen minimalen Netzwerk (Backbone bis Endkunde)
- Backend-Endpunkte zur Topologieabfrage
- Frontend-Visualisierung per Leaflet, Geräte als Marker
- Implementierung SVG-basierter Icons für Gerätetypen

## Phase 3 – Kabel-, Link- und Pfadlogik
- Datenstruktur für Verbindungen in JSON: `links`, `cables`
- Anklickbare Glasfaserverbindungen mit Anzeige von Fasertyp, Dämpfung, Länge etc.
- Interaktive Detailpanels (`CableInfoPanel.jsx`)
- Metrikenvisualisierung pro Link und Pfadabschnitt (z. B. Delay, Loss, Jitter)
- Redundanzsimulation per Dijkstra-basiertem Ausfallmodell
- Kaskadierte Ausfallketten mit Anzeige von Primär- und Backuppfaden

## Phase 4 – CLI-Engine und Konfiguration
- Vollständig interaktive CLI pro Gerät
- Playbook-Runner zur Ausführung von CLI-Skripten
- Konfigurationsspeicherung per `config_store.json` und `config_snapshots`
- Unterstützung für Session-Stack und CLI-Kontextmanagement
- CLI-Diff-Funktion zum Vergleich von Konfigurationsständen

## Phase 5 – CGNAT- und Routingforensik
- NAT-Mapping-Struktur mit IP-, Port-, Zeit- und MAC-Zuordnung
- Rückverfolgbarkeit von Sessions: Webserver → Peering → Core → BNG → OLT → CPE
- Forensik-Ansicht für Ermittlungsfälle oder Netzwerkvorfälle
- Integration von `cgnat_doc.md`, `iproute_cgnat_clear.md` in Simulationslogik

## Phase 6 – Simulation Engine & Szenarien
- Globaler Simulationsschalter im UI und Backend
- Steuerung aller Subsysteme (CLI, Alarme, NAT, Pfade) über Status `simulation_active`
- Integration von definierten Ausfallszenarien (z. B. Fiber Cut, Routing Divergence)
- Optionale Random-Events für Testzwecke
- Schnittstellen für spätere KI-basierte Fehlerauswertung

## Phase 7 – Karten- und Ansichtsmodi
- Interaktive Leaflet-Ansicht mit Geo-Koordinaten
- 2D-Ansicht (abstrakte logische Layer)
- 3D-Topologie (Three.js oder vergleichbar)
- Heatmap-Integration (z. B. Delay in Echtzeit farblich darstellen)
- Gerätestatusvisualisierung im Stil eines NOC-Dashboards

## Phase 8 – UI-Erweiterung & Visualisierungen
- Dashboard mit Widgets (Uhrzeit, Alarmzähler, Gerätestatus)
- Live-Datenpanels pro Gerät
- PathMetricsPanel zur Anzeige aktueller Pfadmetriken
- Dynamischer Umschalter zwischen Layer-, Geo- und Redundanzansicht
- Responsive Dark UI im Cisco-Stil mit Tailwind-kompatiblen Komponenten

## Phase 9 – Exporte, Audits & Dokumentation
- Exportfunktion der Topologie als JSON/PNG/SVG
- Erstellung signierter Log-Dateien (SHA256)
- Export von CLI-Dumps und Audit-Trail per SessionStack
- Markdown-Dokumentation aller Gerätetypen unter `docs/devices/`
- Versionierte Update-Dokumentation unter `docs/update_summary/`

## Phase 10 – Erweiterbarkeit und Pluginstruktur
- Aufbau eines erweiterbaren Pluginsystems für neue Gerätetypen, Szenarien, UI-Komponenten
- WebSocket-Integration für Live-Updates (optional)
- Vorbereitung für Multi-User-Simulation mit Rollen- und Rechteverwaltung
- Implementierung von Test- und Analyse-Schnittstellen für DevOps oder Schulungen
