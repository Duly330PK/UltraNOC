# UltraNOC – Final Feature Set (Stand: Phase 3/4)

## 🟢 1. Benutzer & Authentifizierung
- Login mit JWT (Username + Passwort, access_token)
- Rollenmodell: admin, operator, viewer
- Token Refresh & Logout
- Multi-Faktor-Authentifizierung (optional)
- Multi-Tenant Support mit Mandantenzuweisung

## 🟢 2. Geräteverwaltung & Simulation
- Realistische Gerätetypen (Core Router, Firewall, ONT, OLT etc.)
- Gerätespezifisches CLI (Cisco IOS, Juniper, MikroTik, Huawei)
- LED-/Panel-Visualisierung (TX/RX, Fehleranzeigen)
- Gerätemodelle mit Ports, OS, Status, Position
- Konfigurationshistorie mit Rollback & Diff-Vergleich

## 🟢 3. Netzwerk-Topologie & Verkabelung
- Interaktive Topologie-Karte (SVG/Canvas)
- FiberMap mit realen Dämpfungswerten (dB/km)
- Kaskadenfehler-Logik bei Ausfällen
- Patchpanel/ODF-Darstellung
- VLAN-, Session- und Routing-Sicht

## 🟢 4. Traffic- & Session-Simulation
- Simulierter Nutzertraffic (Web, VoIP, DNS)
- Session-Trace Engine (IP ↔ NAT ↔ MAC ↔ Gerät)
- Traffic Generator (iperf, QoS-Profile)
- CGNAT mit Aging & Pool-Übersicht
- DHCP/DNS Simulator mit Lease-Logs

## 🟢 5. CLI-System & OS-Simulation
- Multi-OS CLI-Engine (SessionRouter, Cisco/Juniper/Huawei)
- CLI-Recorder & Replay-Modul
- OS-spezifische Prompts & Befehlssätze
- YAML-basierte Command Registry
- CLI-Hilfesystem (`?`, Autovervollständigung)
- Kontextverhalten mit SessionStack
- CLI-Playbook Runner (vorkonfigurierte Scripts)
- CLI-Diff & Audit-Trigger bei Änderungen

## 🟢 6. Routing, NAT, VLAN, Policies
- OSPF, BGP (light) & Static Routing
- VLAN-Konfigurationen + Trunk/Access
- NAT/CGNAT-Handling mit vollständiger Sichtbarkeit
- ACL & Zonenregel-Logik über Policy-Engine
- QoS-Klassifizierung (Basis, Erweiterung in Phase 4)

## 🟢 7. Alarmierung & Metriken
- Metriken: CPU, RAM, Traffic, Delay, Loss, Sessions
- Alarme bei Grenzwertüberschreitung
- Kettenreaktions-Logik bei Fehlern
- Auditlog, Accesslog & Alarm-Timeline
- Signierte Logs (SHA256), optional TLS-API-Zugriff

## 🟢 8. Forensik & Rückverfolgung
- CGNAT DeepSearch & Port-Suche
- DHCP-/MAC-/IP-Korrelation
- DPI Flow-Klassifizierung
- Session Traceback mit vollständiger Pfadanalyse
- Signierter Audit-Export (JSON/PDF)

## 🟢 9. Frontend & Visualisierung
- React-basiertes UI mit Tailwind & Cisco-Stil
- Authentifizierter Zugriff mit Rollenfiltern
- Gerätekarten, CLI-Terminal, Statuspanels
- Topologie-Overlay (Fiber, Sessions, VLANs)
- Multitab & Multi-Region Sicht (optional)

## 🟢 10. Simulation & Path-Calculation
- Physikalisch korrekte Link-Simulation (Dämpfung, Delay, Jitter)
- Carrier-Delay & Buffer-Modellierung je Gerät
- Latency-Weight-Routing
- Echtzeit-Pfadvisualisierung im TopologyView
- simulate-Funktionen (fiber-break, ddos etc.)

## 🟢 11. Systemarchitektur & DevOps
- Modularer Backend-Aufbau mit core/, api/, sim_kernel/
- PostgreSQL + SQLAlchemy, ENV-konfigurierbar
- Dockerfile + docker-compose für Dev/Prod
- pytest-Kompatibilität für Unit/Integrationstests
- CI/CD-Vorbereitung via GitHub Actions o. ä.

## 🟢 12. Dokumentation & Erweiterung
- Markdown-Dokumentation aller Module, Geräte, CLI-Befehle
- Downloadbare ZIPs pro Funktionsblock
- Swagger UI & OpenAPI automatisch verfügbar
- Glossar, Gerätevergleich & Feature-Matrix