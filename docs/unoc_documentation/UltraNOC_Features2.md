🧠 UltraNOC – Featureübersicht (Vollständige Zielarchitektur)
1. 🔐 Authentifizierung & Session Management
Feature	Beschreibung	Implementierung
Benutzer-Login	Token-basiert, SessionContext	FastAPI, AuthRouter, AuthContext.jsx
Rollen & Rechte	spätere Trennung (z. B. Admin, Operator)	vorbereitet, noch nicht granular
Protected Routes	Frontend-Schutz für geschützte Ansichten	ProtectedRoute.jsx
Token-Handling	LocalStorage + Logout-Logik	AuthContext, axios Interceptor

2. 🌐 Netzwerk-Topologie & Geo-Visualisierung
Feature	Beschreibung	Implementierung / Plugin
Geräte-Knoten	Geräte auf Karte mit realer Position	Leaflet
Gerätesymbole (Icons)	Gerätetypen mit SVG/DivIcon	getDeviceIcon.js, Leaflet
Glasfaserverbindungen	Verlinkung von Geräten mit Polyline	Leaflet
Redundanzpfade	Primär-/Backup-Pfade farbig, dynamisch	redundancy.py, Leaflet
Klickbare Verbindungen	Zeigt CableInfoPanel mit Details	React, Leaflet
Topologie-Fallback (2D)	Layer- oder Strukturansicht ohne Geo	geplant
Topologie-Import (GeoJSON/JSON)	Manuell oder Dateiimport	vorbereitet (data/topology/*.json)
Simulation eines Netzsegments	z. B. Düsseldorf – Kleve – Rees etc.	core_topology.json, Geo-Koordinaten

3. 📟 Gerätemanagement & CLI
Feature	Beschreibung	Umsetzung
CLI-Terminal je Gerät	Interaktives Terminal mit History	showCLI, CLI-Panels
Gerätekonfig-Speicher	Persistente Configs je Gerät	config_store.py, JSON
CLI-Befehlsinterpreter	Kommando-Registry mit Hilfe etc.	cli_engine, YAML Playbooks (in Planung)
Gerätezustände	Online/Offline mit LED-Farben	Device-Status + MockMetrics
Gerätemetadaten	Gerätetyp, IP, ID, MAC etc.	Topologie-JSON, Popup

4. 📈 Live-Metriken & Pfadbewertung
Feature	Beschreibung	Implementierung
Live-Daten TX/RX	Gerätedurchsatz (bps)	mockMetrics, MetricsPanel
Delay/Loss pro Pfad	Simulierte Qualität pro Hop	path_metrics.py, PathMetricsPanel.jsx
Heatmap-Style	Farbverlauf nach Metrikwert	Tailwind + getColor()-Logik
Jitter-Daten	Optional je Pfadhop	integriert
CLI-Ping-Output (später)	Reale Kommandos wie ping, traceroute	geplant in CLI-Ausgabe

5. 🚨 Alarmierung & Forensik
Feature	Beschreibung	Implementierung
AlarmPanel	Zeigt aktive Alarme oben links	AlarmPanel.jsx
AlarmSeverity	Farblich (critical, warning, info)	Tailwind-Klassen
CGNAT-Trace	Mapping von IP/Port/MAC	iproute_cgnat_clear.md, nat_sessions
Forensische Rückverfolgung	End-to-End Audit (CPE → Webserver)	vorbereitet (NAT + Routing Trace Engine)
Logformate	z. B. NAT MAP: Einträge	geplant für Audit-Panel

6. 📄 Ticketing & Audit Logs
Feature	Beschreibung	Implementierung
Ticket-Modul	Tickets erstellen bei Alarm	tickets-Tabelle, UI noch ausstehend
Audit Log	Signierte Logs (SHA256)	audit_logs, geplant TLS
Snapshots	Konfigschnappschüsse bei Änderung	config_snapshots
Trigger Audit	Änderungen führen zu Eventlogs	noch in Planung (per CLI-Änderung)

7. ⚙️ Simulation & Steuerung
Feature	Beschreibung	Umsetzung
Simulation Start/Stop	Globaler Simulationszustand	simulation_control.py, Topbar-Schalter
Szenario-Schalter	Später: gezielte Events aktivieren	vorbereitet
Fiber Cut / Failure Injection	z. B. simulate fiber-break	geplante Flags in Pfadengine
Zufallsereignisse	z. B. Gerät fällt aus	optional
Kettenreaktion	Redundanzwechselsimulation	redundancy.py (dijkstra + fallback)

8. 📤 Export & Import
Feature	Beschreibung	Status
Topologie-Export	JSON-Export der Netzstruktur	/api/topology/
Config-Export	Gerätekonfigurationen	config_store.json
CLI-Export	Playbook Runner YAML	vorbereitet
Device-Import	Modularer Geräteaufbau später	geplant

9. 🎨 Benutzeroberfläche (UI)
Feature	Beschreibung	Tools
Dark Mode UI	Cisco-NOC-inspiriertes Design	Tailwind CSS
Responsive SPA	Flexibles Layout	React + Vite
Dashboard	Übersicht über Geräte, Metriken	/dashboard
Sidebar + Header	Navigation mit Icons	Sidebar.jsx, Header.jsx
CLI Panel	Dynamisches CLI-Modul pro Gerät	Popup UI
Heatmap/Charts	Metriken visuell dargestellt	Tailwind, später chart.js, three.js
Modale Fenster	InfoPanels, Alarme etc.	Tailwind UI

10. 📦 Backend-Architektur & Datenbank
Feature	Beschreibung	Tools
FastAPI	Modulares Router-Backend	routers/*.py
SQLAlchemy	ORM für Geräte, Sessions etc.	models/, schemas/
PostgreSQL	Datenbank für alle Module	.env, docker, init.sql
Seed-Daten	Geräte, Metriken, User	init_*.sql
Modularität	Jeder Bereich eigener Router	routers/device_metrics.py, etc.
API Docs	Swagger Doku automatisch	/docs

11. 📁 Dateien & Strukturen
Typ	Speicherort
Geräte-Doku	docs/devices/*.md
Updateberichte	docs/update_summary/*.md
CGNAT/Forensik	docs/cgnat_*.md
Simulationen	scenarios/*.json (später)
Karten/Leaflet	public/leaflet/, Map/*.jsx
Icons	assets/icons/, dynamisch per JS

