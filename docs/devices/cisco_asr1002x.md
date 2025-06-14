✅ C:\noc_project\UltraNOC\docs\devices\cisco_asr1002x.md
markdown
Copy
Edit
# Cisco ASR1002-X – Core Router

## Überblick
- **Hersteller**: Cisco
- **Modell**: ASR1002-X
- **OS**: Cisco IOS XE
- **Rolle**: Core-Routing, BGP/OSPF, NAT, CGNAT
- **Geräteklasse**: Backbone-Node
- **Redundanz**: Dual Uplink, Hot Standby, HSRP-ready
- **Physisch**: Rackmount 1RU, Frontpanel mit LED-Anzeige (Status, Active, Alarm, PWR)

## Ports
| Port     | Typ              | Beschreibung           | LED-Anzeige     |
|----------|------------------|------------------------|-----------------|
| Gi0/0/0  | GigabitEthernet  | Uplink Richtung RZ01   | TX/RX, Status   |
| Gi0/0/1  | GigabitEthernet  | Redundanz (HSRP Link)  | TX/RX, Status   |
| Mgmt0    | FastEthernet     | Management-Port        | Activity        |
| CON      | Konsolenport     | CLI-Zugang             | -               |

## CLI-Beispiele

```cli
ASR1002X> enable
ASR1002X# configure terminal
ASR1002X(config)# interface Gi0/0/0
ASR1002X(config-if)# ip address 10.255.1.1 255.255.255.0
ASR1002X(config-if)# no shutdown
ASR1002X(config-if)# exit
ASR1002X(config)# router ospf 100
ASR1002X(config-router)# network 10.255.1.0 0.0.0.255 area 0
ASR1002X(config-router)# exit
ASR1002X(config)# ip nat inside source list 10 interface Gi0/0/0 overload
ASR1002X(config)# end
ASR1002X# write memory
Konfiguration
plaintext
Copy
Edit
hostname ASR1002X
!
interface Gi0/0/0
 description Uplink-RZ01
 ip address 10.255.1.1 255.255.255.0
 no shutdown
!
interface Gi0/0/1
 description Redundanz Link
 ip address 10.255.1.2 255.255.255.0
 standby 1 ip 10.255.1.254
!
router ospf 100
 network 10.255.1.0 0.0.0.255 area 0
!
ip nat inside source list 10 interface Gi0/0/0 overload
!
access-list 10 permit 192.168.0.0 0.0.0.255
Metriken
Metrik	Wert	Schwelle
CPU Load	12 %	Warnung > 85 %
RAM Nutzung	2.1 GB / 8.0 GB	-
TX/RX Gi0/0/0	820 Mbps / 910 Mbps	-
Temperatur	43 °C	Kritisch > 70 °C
NAT-Sessions	15 230 aktiv	Max: 1 Mio.

Fehler & Alarme
%BGP-5-ADJCHANGE: neighbor 10.0.1.1 Down

High CPU Usage > 85%

NAT Session Table near capacity

HSRP Standby lost, failover initiated

Interface Gi0/0/0 down – simulated fiber break

Simulation
🔄 CLI-Befehle steuern OSPF/NAT-Status

🧠 Topologie-Overlay zeigt aktiven Pfad

🔁 Redundanzpfad (Gi0/0/1) übernimmt bei Fehlern

🚨 Fehlerstatus triggert Alarme im Dashboard

🌐 Geo-Knoten (Stadt/RZ) auf Map + Layer-Ansicht

mathematica
Copy
Edit

Alt:
CLI-Stil: Cisco IOS XE

Physikalische Merkmale: LEDs, Ports

Funktionen: Routing, NAT, CGNAT, BGP, OSPF

Fehler, Alarmierung, Simulationseinfluss, Verkabelung

Realistische Beispiele aus der Praxis von ISPs wie Deutsche Glasfaser

📄 Pfad:
C:\noc_project\UltraNOC\docs\devices\cisco_asr1002x.md

markdown
Copy
Edit
# Cisco ASR1002-X – Core Router mit CGNAT

## Überblick

| Attribut           | Wert                            |
|--------------------|----------------------------------|
| Hersteller         | Cisco                            |
| Modell             | ASR1002-X                        |
| OS                 | Cisco IOS XE                     |
| Rolle              | Core Router / CGNAT Gateway      |
| Einsatzbereich     | Backbone-Edge, BNG, NAT          |
| Stromversorgung    | Dual PSU, Hot-Swap               |
| Kühlung            | Front-to-Back Airflow            |
| LED-Anzeigen       | PWR, STATUS, ACTIVE, FAN, PSU    |

---

## Ports & Interfaces

| Port       | Typ              | Beschreibung                     |
|------------|------------------|----------------------------------|
| Gi0/0/0    | GigabitEthernet  | Upstream ISP                     |
| Gi0/0/1    | GigabitEthernet  | Backup-Uplink                    |
| Gi0/0/2    | GigabitEthernet  | Richtung BRAS                    |
| Mgmt0      | Ethernet         | Out-of-Band Management           |

---

## CLI-Beispiele (IOS XE)

```cli
ASR1002-X> enable
Password:
ASR1002-X# show version
Cisco IOS XE Software, Version 17.3.5
Uptime: 3 days, 22 hours

ASR1002-X# configure terminal
ASR1002-X(config)# interface Gi0/0/0
ASR1002-X(config-if)# ip address 192.0.2.1 255.255.255.0
ASR1002-X(config-if)# no shutdown
ASR1002-X(config-if)# exit

ASR1002-X(config)# access-list 1 permit 10.0.0.0 0.0.255.255
ASR1002-X(config)# ip nat inside source list 1 interface Gi0/0/0 overload

ASR1002-X(config)# interface Gi0/0/1
ASR1002-X(config-if)# ip nat outside
ASR1002-X(config)# interface Gi0/0/2
ASR1002-X(config-if)# ip nat inside

ASR1002-X(config)# exit
ASR1002-X# show ip nat translations
Pro  Inside global      Inside local       Outside local      Outside global
tcp 192.0.2.10:1025     10.0.0.5:1025      93.184.216.34:443  93.184.216.34:443
tcp 192.0.2.10:1026     10.0.0.6:1026      142.250.74.78:443  142.250.74.78:443
Status & Metriken
Metrik	Beispielwert	Einheit
CPU Load	43%	Prozent
TX-Pegel Port 0	-4.2	dBm
RX-Pegel Port 0	-2.9	dBm
Temperatur	41.5	°C
NAT Sessions (live)	48.326	Sessions
NAT Table Util.	19%	Prozent

Fehlerszenarien & Alarme
Szenario	Alarmmeldung
BGP-Peering Down	%BGP-5-ADJCHANGE: neighbor 192.0.2.2 Down
NAT Table 95% voll	Warning: NAT session table nearing capacity
Temperatur > 70°C	ALARM: High temperature on ASIC
CPU > 85%	Process interrupt due to CPU Overload
RX-Pegel < -20 dBm	LinkDown due to optical power loss

Verkabelung / Topologie
Gi0/0/0 → Provider-Edge Router (UPLINK)

Gi0/0/1 → Redundanzlink zum zweiten ASR

Gi0/0/2 → Richtung BNG oder Aggregation-Switch

Mgmt0 → Management VLAN (Out-of-Band Zugriff)

Simulationseinfluss
CLI-Befehle wirken direkt auf Routing- & NAT-Simulator

NAT Table ist dynamisch und füllt sich je nach Userload

Fehler (Link Down, NAT Exhaustion) wirken auf Dashboard & Alarme

NAT Mapping Table und Port Utilization im LiveView sichtbar

Realistische Betriebsmodi
Dual NAT-Modus: PAT (Port Address Translation) + Static NAT

CGNAT: NAT44 mit Session Aging & Poolverwaltung

BGP/OSPF Routing: Echtzeit-Routenanzeige mit RouteMap-Simulation

Konfig-Snapshots werden bei write memory erzeugt

Visualisierung (Frontend)
LED-Felder für: Power, Status, Fan, Temp

Ports: RX/TX Balken, Fehlerzählung, CRC

NAT-Sessions pro Pool & Slot einsehbar

CLI-Terminal voll interaktiv (Autovervollständigung, Playbooks)

Hinweise zur Umsetzung
Prompts: ASR1002-X>, ASR1002-X#, ASR1002-X(config)#

Simulation: Befehle lösen interne Events aus (z. B. interface shutdown)

CLI unterscheidet zwischen show, conf, debug, clear, reload

Jede Eingabe beeinflusst Zustand & UI-Feedback

TODO (Folgeversionen)
NAT Session Aging im Live-Modus simulieren

Fragmentierte IP-Header + Overload Testing

Exportfunktion für CGNAT-Logs