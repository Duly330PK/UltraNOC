NEUER:
# Huawei MA5800-X17 – Optical Line Terminal (OLT)

## Überblick
- **Hersteller**: Huawei
- **Modell**: MA5800-X17
- **OS**: Huawei VRP (OLT-Anpassung)
- **Einsatz**: GPON/XG-PON Aggregation, Endkundenanbindung, Fiber Access
- **Besonderheit**: Multi-Service Aggregation Platform (Access Gateway)

---

## Ports

| Port            | Typ        | Beschreibung                  |
|-----------------|------------|-------------------------------|
| gpon 0/1/1       | GPON       | Fiber Downstream zu ONTs      |
| gpon 0/1/2–16    | GPON       | weitere PON-Ports             |
| uplink 0/9/0     | 10GE SFP+  | Richtung Aggregation Switch   |
| uplink 0/9/1     | 10GE SFP+  | Redundanter Uplink            |
| eth 0/0/0        | Ethernet   | Management-Port               |
| console          | RS232      | Serielle Konsole              |

---

## CLI-Beispiele

```cli
MA5800> enable
MA5800# display board 0
Slot 0
Board Type : H901MPLA
Run Status : Normal
Port Number: 16 GPON

MA5800# display ont info 0 1
ONT-ID: 1
Status: online
RX Power: -22.5 dBm
TX Power: 3.1 dBm
Distance: 5.3 km
...

MA5800# interface gpon 0/1
MA5800(gpon-0/1)# ont add 1 sn-auth "HWTC12345678" omci ont-lineprofile-id 10 ont-srvprofile-id 20
MA5800(gpon-0/1)# ont commit 1

NEU:
# Huawei MA5800-X17 – OLT (Optical Line Terminal)

## Überblick
- **Hersteller**: Huawei
- **Modell**: MA5800-X17
- **OS**: Huawei VRP (Versatile Routing Platform)
- **Einsatz**: GPON-Zugang, Aggregation, Triple Play
- **Rolle**: OLT mit PON-Splitterverwaltung & VLAN-Stacking
- **Physisch**: 17 Slots, 2U Rackmount, Status-LEDs für Power, Alarm, Active, PON, Uplink

## Ports & Slots
| Slot | Typ         | Beschreibung             | LEDs         |
|------|-------------|--------------------------|--------------|
| Uplink0 | 10GE SFP+ | Aggregation ins Backbone | TX/RX, Link  |
| PON1   | GPON       | Splitter 1:64 (Kunden)   | PON-LEDs     |
| PON2   | GPON       | Backup-Splitter          | PON-LEDs     |
| MGMT   | FastEthernet | Lokales Management    | Status       |

## CLI-Beispiele (VRP)

```cli
<Huawei> system-view
[Huawei] interface gpon 0/1
[Huawei-gpon0/1] onu 1 type HG8245T sn 4857544321654321
[Huawei-gpon0/1] onu 1 port 1 eth 1
[Huawei-gpon0/1] quit
[Huawei] vlan batch 100 200
[Huawei] interface vlanif 100
[Huawei-Vlanif100] ip address 192.168.100.1 255.255.255.0
[Huawei-Vlanif100] quit
[Huawei] save
Konfiguration
plaintext
Copy
Edit
#
sysname MA5800
vlan batch 100 200
#
interface gpon 0/1
 onu 1 type HG8245T sn 4857544321654321
 onu 1 port 1 eth 1
#
interface vlanif 100
 ip address 192.168.100.1 255.255.255.0
#
igmp config vlan 100
#
dhcp enable
Metriken
Metrik	Wert	Schwelle
ONT Sessions	62 von 64 aktiv	Max: 64
TX/RX Uplink0	4.2 Gbps / 3.8 Gbps	-
CPU-Auslastung	27 %	> 85 % kritisch
Temperatur	39 °C	> 70 °C kritisch
VLANs aktiv	2 (100, 200)	-

Fehler & Alarme
ONU offline: SN 4857544321654321

VLAN 200 DHCP conflict detected

GPON port 0/1 signal loss

High CPU > 85%

Split ratio exceeded on PON1

Simulation
🔌 simulate fiber-break auf PON1 trennt 64 ONTs

🔄 CLI-Konfig ändert dynamisch Routing/VLAN-Zuordnung

🚨 Alarme auf ONT-Level → Kundenstörungen

📍 Darstellung: Aggregation-Node mit PON-Ast-Knoten

🔍 ONT-Knoten via SessionTrace rückverfolgbar

markdown
Copy
Edit

### 🔧 Backend/Simulation:
Die Huawei MA5800-X17 wird künftig im `device_inventory`, `cli_playback` und `topology` als Typ `"HuaweiOLT"` geführt – inklusive:

- `cli_registry/huawei.yaml` (noch zu erstellen)
- Topology-Node `type: OLT`
- Rolle: `"access-aggregation"`
- Geo-Koordinaten-fähig (später Sandbox-Setzung)

---

**Nächster Schritt (Gerät 3):**  
→ `Juniper MX204` (BNG / BRAS)  
→ CLI, Traffic-Session, DHCP/NAT-Rolle, Redundanz möglich
ALT:

# Huawei MA5800-X17 – Optical Line Terminal (OLT)

## 🧾 Geräteübersicht
- **Hersteller:** Huawei
- **Modell:** MA5800-X17
- **Betriebssystem:** Huawei VRP (Versatile Routing Platform)
- **Einsatzrolle:** GPON/XG-PON OLT für FTTx-Netze (Fiber to the Home)
- **Netzebene:** Access/Aggregation
- **Montage:** 19" Rack, 6U
- **Stromversorgung:** Redundant, 220 V/48 V DC
- **Management:** Telnet, SSH, SNMP, WebUI

## 🔌 Ports & Interfaces

| Steckplatz | Bezeichnung         | Typ              | Beschreibung                       |
|------------|---------------------|------------------|------------------------------------|
| SLOT0–SLOT16 | Service Boards     | GPON / XG-PON    | Uplink zu ONTs                     |
| SLOT17     | Main Control Board  | SCUN             | Steuerung & Management             |
| SLOT18     | Uplink Board        | GE/10GE          | Uplink zu Aggregation/Core         |
| CONSOLE    | RJ45                | Serielle Wartung | Lokale CLI-Konsole                 |
| ETH0       | Fast Ethernet       | Mgmt-Port        | Out-of-Band Management             |

## 💡 LED-Anzeigen

| LED         | Farbe     | Bedeutung                             |
|-------------|-----------|----------------------------------------|
| RUN         | Grün blinkend | System läuft normal                 |
| ALM         | Rot       | Kritischer Alarm                      |
| PWR1/PWR2   | Grün      | Stromversorgung aktiv                 |
| PON[x]      | Grün/Gelb | Status der GPON-Ports (LOS, ACT usw.) |
| ETH         | Grün      | Management-Link aktiv                 |

## 🖥️ CLI-Beispiele (Huawei VRP)

```cli
<Huawei> display version
Huawei Versatile Routing Platform Software
VRP (R) software, Version 5.170 (MA5800 V300R018C10SPC100)

<Huawei> enable
<Huawei> system-view
[Huawei] interface gpon 0/1
[Huawei-gpon0/1] display ont info 0 all
----------------------------------------------------
ONT-ID  State  RunState  LastUpTime   Description
0       online active    2024-12-01   ONT_HG8245H_1
1       offline down     ----         ----

[Huawei-gpon0/1] ont reset 1
Warning: This operation will reboot ONT 1. Continue? [Y/N]: y

[Huawei] display alarm active
-------------------------------------------------------------------------------
ID  Level  Alarm Type       Description                 Affected Object
1   CRIT   LOS              Loss of Signal              gpon0/1/1
2   MAJOR  Dying Gasp       Power fail ONT              gpon0/1/2
-------------------------------------------------------------------------------
⚙️ Konfigurationsbeispiel
cli
Copy
Edit
[Huawei] vlan 100
[Huawei-vlan100] quit

[Huawei] interface gpon 0/1
[Huawei-gpon0/1] ont add 1 sn-auth "HWTC12345678" omci ont-lineprofile-id 10 ont-srvprofile-id 10 desc "ONT_1"
[Huawei-gpon0/1] ont port native-vlan 1 eth 1 vlan 100
[Huawei] interface vlanif 100
[Huawei-Vlanif100] ip address 192.168.1.1 255.255.255.0
📉 Betriebsmetriken
Metrik	Beispielwert	Beschreibung
TX Power (OLT)	+2.0 dBm	Sendestärke
RX Power (OLT)	–19.5 dBm	Empfangsstärke vom ONT
CPU-Auslastung	43 %	Steuerprozessorlast
ONT Sessions	512	Aktive ONT-Verbindungen
GPON Alarmzahl	3 aktiv	Aktuelle Alarme

⚠️ Fehlerszenarien & Alarme
Alarmtyp	Ursache	Verhalten im System
LOS (Loss of Signal)	Faserschaden, ONT offline	Kritischer Alarm + Port rot
Dying Gasp	ONT Stromverlust	Log-Eintrag + Alarm
High CPU Usage	>85 % Systemauslastung	Gelber Alarm, CLI-Warnung
Slot Failure	Service-Board nicht erkannt	Slot-LED blinkt, Alarm aktiv

🔗 Topologie & Verknüpfung
Upstream: 10GE-Uplink zu Aggregation-Switch (z. B. Huawei S6720)

Downstream: GPON-Verbindung zu 1:64-Splitter, ONTs (HG8245H etc.)

Verkabelung: über Patchpanel/ODF → FiberMap sichtbar

Verbundene Objekte: VLAN-Zuweisung, DHCP-Zuordnung, SessionTrace

🧪 Simulationseinfluss
Aktion im Simulator	Effekt
ont reset	Sitzung des ONT bricht ab, Alarm generiert
simulate fiber-break	LOS für alle ONTs auf Port x
vlan remove	Sessionverlust, neue IP-Zuweisung via DHCP
cpu overload	Response Delay erhöht, Alarme aktiv

🧰 Erweiterte Features
FEC (Forward Error Correction)

DBA (Dynamic Bandwidth Allocation)

Loop Detection & Storm Control

PPPoE Relay für Triple-Play Dienste

DHCP Option 82 Forwarding

📍 Beispiel für Gerätebeziehung
yaml
Copy
Edit
device_id: olt-huawei-1
model: MA5800-X17
links:
  - to: agg-switch-huawei-6720
    type: 10GE
  - to: splitter-01
    type: gpon
    ratio: 1:64