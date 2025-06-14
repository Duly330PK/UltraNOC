NEU:
# Juniper MX204 – BNG / BRAS (Broadband Network Gateway)

## Überblick
- **Hersteller**: Juniper
- **Modell**: MX204
- **OS**: Junos OS
- **Einsatz**: Breitband-Zugangskonzentrator, PPPoE, DHCP, NAT, L2TP, CGNAT
- **Rolle**: BRAS (Session Aggregation), Edge-Routing
- **Physisch**: 1HE, 4×100GE QSFP28 + 8×10GE, Status-LEDs (Alarm, Power, Online, TX/RX)

## Ports
| Port     | Typ     | Beschreibung             |
|----------|---------|--------------------------|
| xe-0/0/0 | 10GE    | Uplink zur Core          |
| xe-0/0/1 | 10GE    | Redundanzlink            |
| ge-0/0/2 | 1GE     | PPPoE Access (SessionIn) |
| ge-0/0/3 | 1GE     | Management               |

## CLI-Beispiele (Junos)

```cli
root> show interfaces terse
Interface               Admin Link Proto    Local                 Remote
ge-0/0/2                up    up   pppoe    172.16.0.1

root> show pppoe sessions
Session ID: 0x04A1
State: Active
Interface: ge-0/0/2.0
Remote MAC: 00:11:22:33:44:55
IP Address: 10.100.10.5
Uptime: 03:22:18

root> configure
[edit]
set interfaces ge-0/0/2 unit 0 family inet address 172.16.0.1/24
set routing-options static route 0.0.0.0/0 next-hop 10.0.0.1
set services nat rule-set OUTBOUND from zone trust to zone untrust rule NAT_ALL match source-address 10.0.0.0/8 then translated source pool NAT_POOL
set security nat source pool NAT_POOL address 100.64.1.0/24
commit
Konfiguration
plaintext
Copy
Edit
interfaces {
    ge-0/0/2 {
        unit 0 {
            family inet {
                address 172.16.0.1/24;
            }
        }
    }
}
services {
    pppoe;
    dhcp-local-server {
        group access {
            interface ge-0/0/2.0;
        }
    }
}
security {
    nat {
        source {
            pool NAT_POOL {
                address {
                    100.64.1.0/24;
                }
            }
            rule-set OUTBOUND {
                from zone trust;
                to zone untrust;
                rule NAT_ALL {
                    match {
                        source-address 10.0.0.0/8;
                    }
                    then {
                        translated {
                            source pool NAT_POOL;
                        }
                    }
                }
            }
        }
    }
}
Metriken
Metrik	Wert	Schwelle
PPPoE Sessions	912 aktiv	Max: 2048
NAT Table Usage	78 %	> 90 % kritisch
CPU Load	33 %	> 85 %
TX/RX Rate	6.8 Gbps / 5.1 Gbps	-
DHCP Lease Conflicts	1	> 10 kritisch

Alarme & Fehler
%PPPoE Session Timeout: session 0x04A1

%NAT_POOL exhausted

%DHCP lease conflict on IP 10.100.10.8

%High CPU detected (above 90%)

Simulationseinfluss
📡 simulate session-flood → NAT + DHCP überlastet

🔄 Realtime-Sessions steuerbar über CLI

🚨 Fehleralarme (Lease Conflict, NAT Exhausted)

🔍 Rückverfolgung via SessionTrace: ONT → BRAS → IP

📍 Darstellung: Aggregation-/Edge-Knoten mit NAT-Logik

yaml
Copy
Edit

### 🔧 Backend-Anbindung

- Gerätetyp: `"JuniperBNG"`
- Simulation: SessionTable, NAT-Engine, DHCP-LeaseMap
- UI: NAT/Session-Dashboard + CLI-Modul

---
ALT:
# Juniper MX204 – BRAS / Broadband Network Gateway

## Überblick
- Hersteller: Juniper Networks
- Modell: MX204
- OS: Junos OS (z. B. 20.4R3-S2)
- Einsatz: BNG / BRAS, CGNAT, DHCP, PPPoE, Edge-Routing

## Physische Eigenschaften
| Merkmal         | Beschreibung                                    |
|------------------|-------------------------------------------------|
| LEDs             | Status, Alarm, Fan, Ports (Link/Act)            |
| Formfaktor       | 1U, kompaktes Gehäuse für hohe Dichte           |
| Stromversorgung  | Redundant, Hot-Swap-fähig                       |
| Lüfter           | Variable, temperaturgesteuert                  |
| Management       | Console + Mgmt-Port (me0)                       |

## Ports
| Port        | Typ         | Funktion                          |
|-------------|-------------|-----------------------------------|
| xe-0/0/0    | 10G SFP+     | Uplink zu Core                    |
| xe-0/0/1    | 10G SFP+     | Downlink zu Aggregation (z. B. EX)|
| me0         | Mgmt        | Management Interface              |

## CLI-Beispiele (Junos OS)
```cli
user@mx204> show chassis hardware
Item             Version  Part number  Serial number     Description
Chassis                                MX204-CHAS
Midplane         REV 07   750-070590   xxxxxx            MX204 Midplane
FPC 0            REV 04   750-070592   xxxxxx            4x10GE, 2x100GE

user@mx204> show interfaces terse
Interface        Admin Link Proto    Local
xe-0/0/0         up    up
xe-0/0/1         up    up
me0              up    up   inet     10.0.1.1/24

user@mx204> show services nat statistics
Active Sessions : 6000
Peak Sessions   : 14500
Dropped Packets : 1200

user@mx204> show system alarms
2 alarms currently active
Major  Host  Temperature Sensor 85°C
Minor  NAT Session Table 95% Utilization
Simulationseinflüsse
simulate nat_overload → Sessions werden nicht mehr aufgebaut

simulate reboot → 10 Sekunden Neustart mit Ausfall aller Verbindungen

simulate dhcp_failure → Clients erhalten keine IPs

Alarmanzeige in Dashboard + CLI

Fehlerszenarien
NAT-Table überfüllt

CPU-Saturation bei 100GE Traffic

PPPoE Session Timeout / RADIUS Fail

Temperatur-Überhitzung durch Lüfterausfall

YAML-Verknüpfung
yaml
Copy
Edit
id: bras-juniper-mx204
type: BRAS
vendor: Juniper
model: MX204
os: Junos
ports:
  - id: xe-0/0/0
    type: sfp+
    to: core-cisco-asr1002x
  - id: xe-0/0/1
    type: sfp+
    to: switch-juniper-ex4300-01
metrics:
  nat_sessions: 6000
  nat_peak: 14500
  cpu: 78
  temp: 85
alarms:
  - type: temperature
    level: major
  - type: nat_table
    level: minor