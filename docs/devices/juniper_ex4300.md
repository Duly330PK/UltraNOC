# Juniper EX4300 – Metro Aggregation Switch

## Überblick
- Hersteller: Juniper
- Modell: EX4300-48T
- OS: Junos OS (z. B. 21.1R3)
- Einsatz: Metro Aggregation, VLAN-Stacking, DHCP Relay, L3-Switching

## Physische Eigenschaften
| Merkmal         | Beschreibung                                |
|------------------|---------------------------------------------|
| LEDs             | System, Alarm, Fan, Power, Ports (Link/Act) |
| Formfaktor       | 1U, Rackmontage                             |
| Lüfter           | Front-to-Back Airflow                       |
| Redundanz        | Dual PSU möglich                            |

## Ports
| Port-ID   | Typ               | Beschreibung              |
|-----------|------------------|---------------------------|
| ge-0/0/0  | 1G RJ-45          | Access VLAN Kunden CPE    |
| ge-0/0/1  | 1G RJ-45          | Access VLAN Kunden CPE    |
| xe-0/1/0  | 10G SFP+          | Uplink zu BRAS            |
| me0       | Management-Port   | Out-of-Band Zugriff       |

## CLI-Beispiele (Junos OS)
```cli
root@ex4300> show interfaces terse
Interface        Admin Link Proto  Local                  Remote
ge-0/0/0         up    up
ge-0/0/1         up    up
xe-0/1/0         up    up
me0              up    up    inet  10.0.0.10/24

root@ex4300> show vlan
Name         Tag   Interfaces
customers    100   ge-0/0/0.0, ge-0/0/1.0
uplink       200   xe-0/1/0.0

root@ex4300> show system alarms
No alarms currently active

root@ex4300> show system resource-utilization
CPU utilization          : 23 percent
Memory utilization       : 61 percent
Fehlerszenarien
Interface-Fehler: ge-0/0/0 → Link Down

VLAN-Mismatch mit OLT

DHCP Relay Timeout

CPU Spikes bei Broadcast Storms

Simulationseinflüsse
VLAN Tags beeinflussen Session Trace / DHCP-Leases

Interface-Failure wird visuell & CLI-seitig dargestellt

simulate dhcp_stall blockiert Lease-Vergabe temporär

YAML-Verknüpfung
yaml
Copy
Edit
id: switch-juniper-ex4300-01
type: L3Switch
vendor: Juniper
model: EX4300
os: Junos
ports:
  - id: xe-0/1/0
    type: sfp+
    to: bras-juniper-mx204
  - id: ge-0/0/0
    type: ethernet
    to: ont-huawei-hg8245h-01
vlans:
  - id: 100
    name: customers
  - id: 200
    name: uplink
status:
  cpu: 23
  memory: 61
alarms: []
Empfehlungen
VLAN-Handling in Simulation abbilden

DHCP Relay Verhalten simulieren

Optional: LACP, RSTP, LLDP zur Netzanalyse