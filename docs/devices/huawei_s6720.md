NEU: # Huawei S6720-30C-EI – Metro Aggregation Switch

## Überblick
- **Hersteller:** Huawei
- **Modell:** S6720-30C-EI
- **Betriebssystem:** VRP (Versatile Routing Platform)
- **Einsatzbereich:** L2/L3 Aggregation, VLAN Trunking, QoS, Stack

## Ports
| Port       | Typ               | Beschreibung              |
|------------|--------------------|---------------------------|
| Gig0/0/1   | GigabitEthernet    | Uplink zum Core           |
| Gig0/0/2   | GigabitEthernet    | Redundanter Uplink        |
| 10GE1/0/1  | 10 Gigabit Ethernet| High-Speed Aggregation    |
| ETH        | Management         | Lokaler Zugriff           |

## CLI-Beispiele (Huawei VRP)
```cli
<Huawei> system-view
[Huawei] interface GigabitEthernet 0/0/1
[Huawei-GigabitEthernet0/0/1] port link-type trunk
[Huawei-GigabitEthernet0/0/1] port trunk allow-pass vlan 100 200
[Huawei-GigabitEthernet0/0/1] quit
[Huawei] vlan batch 100 200
[Huawei] interface vlanif 100
[Huawei-Vlanif100] ip address 192.168.100.1 255.255.255.0
Metriken & Statusfelder
CPU-Last, Speicherauslastung, Temperatur

Port TX/RX (bps, Fehler, CRCs)

VLAN-Mapping & Trunk-Status

Stack-ID & Role (Master/Slave)

Alarme & Fehler
%LINK-5-CHANGED: Interface 10GE1/0/1 changed state to down

%VLAN-4-CONFLICT: VLAN ID conflict detected

%STACK-3-SWITCHOVER: Master switchover initiated

Physikalische Darstellung
LEDs: SYS, STAT, STK, PWR, ALM

Ports: 24x GE, 6x 10GE SFP+

Stack-Modus: Unterstützt iStack

Simulationseinfluss
VLAN-Fehlkonfiguration → Broadcast Storm

Port Down → Trunk-Ausfall, Redundanz-Pfad greift

CLI-Aktionen wirken sich direkt auf das Dashboard aus

Topologie-Verknüpfungen
Upstream: Core Router (Cisco ASR1002-X)

Downstream: OLT Huawei MA5800-X17
ALT:

# Huawei S6720 – Aggregation Switch

## Überblick
- **Hersteller**: Huawei
- **Modell**: S6720-30C-EI-24S-AC
- **OS**: Huawei VRP
- **Einsatz**: Aggregation Layer, Metro Ethernet, VLAN-Backbone
- **Besonderheit**: Unterstützt QinQ, STP/MSTP, 10G Uplinks

---

## Ports

| Port         | Typ               | Beschreibung               |
|--------------|------------------|----------------------------|
| XGigabit0/0/1–24 | SFP+ (10G)     | Uplink / Access Ports      |
| GigabitEthernet0/0/0 | RJ45 (Mgmt) | Management-Port            |
| Console      | RJ45              | CLI-Zugriff über RS232     |

---

## CLI-Beispiele

```cli
<Huawei> display interface brief
PHY: physical
*down: administratively down
(l): loopback

Interface                         PHY   Protocol InUti OutUti   inErrors  outErrors
XGigabitEthernet0/0/1             up    up        10%    15%          0          0
XGigabitEthernet0/0/2             up    up         8%    12%          0          0
GigabitEthernet0/0/0              up    up         0%     0%          0          0

<Huawei> system-view
[Huawei] interface XGigabitEthernet0/0/1
[Huawei-XGigabitEthernet0/0/1] port link-type trunk
[Huawei-XGigabitEthernet0/0/1] port trunk allow-pass vlan 10 20 30
[Huawei-XGigabitEthernet0/0/1] quit
[Huawei] vlan batch 10 20 30
Status & Metriken
CPU-Last: 32 %

Temperatur: 43 °C

TX/RX: pro Port abrufbar

Fan-Status: normal

LEDs:

SYS (grün): OK

ALM (aus): kein Alarm

Port LEDs: je nach TX/RX-Aktivität grün blinkend

Konfigurationsbeispiel
cli
Copy
Edit
[Huawei] vlan batch 100 200
[Huawei] interface vlanif 100
[Huawei-Vlanif100] ip address 192.168.1.1 255.255.255.0
[Huawei-Vlanif100] quit
[Huawei] interface XGigabitEthernet0/0/3
[Huawei-XGigabitEthernet0/0/3] port link-type access
[Huawei-XGigabitEthernet0/0/3] port default vlan 100
Fehlerszenarien
%LINK-3-UPDOWN: Interface down

%VLAN-4-CONFIG: VLAN mismatch

High CPU durch Broadcast Storm

Temperatur > 70 °C

Verbindungen
XGigabit0/0/1 → Core Router (Uplink)

XGigabit0/0/2 → OLT (Zugangsnetz)

XGigabit0/0/3–24 → ONTs, BRAS, DHCP

Simulationseinfluss
VLAN-Tagging wirkt auf Routing/NAT

Fehlerstatus lösen Alarm und visuelle Signale aus

Traffic-Verkehr simuliert TX/RX per Port

Konfigurationsänderungen können Paketverlust simulieren

Zusatzfeatures
QinQ (802.1ad) für Service Trennung

MSTP für redundante L2-Pfade

LLDP aktiv für Topologie Discovery

DHCP Relay Option 82

