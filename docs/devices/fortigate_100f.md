# FortiGate 100F – Security Gateway

## Überblick
- Hersteller: Fortinet
- Modell: FortiGate 100F
- OS: FortiOS 7.x
- Einsatz: Firewall, NAT, DPI, VPN, Policy Control (ISP-Core/Edge)

## Physische Eigenschaften
| Merkmal        | Beschreibung                          |
|----------------|---------------------------------------|
| Formfaktor     | 1U Rackmount                          |
| Ports          | 18x GE RJ45, 2x 10GE SFP+, 2x GE MGMT |
| LEDs           | Power, Status, Port-Activity, Alarm   |
| Management     | Web-GUI (443), SSH (22), CLI (via MGMT)|

## Ports
| Port      | Typ           | Funktion                        |
|-----------|----------------|---------------------------------|
| port1     | GE RJ45       | WAN Uplink                      |
| port2     | GE RJ45       | LAN / Trust Zone                |
| port3–16  | GE RJ45       | Optional Segmente               |
| SFP1-2    | 10GE SFP+     | Highspeed-Uplink (z. B. BNG)     |
| MGMT      | GE RJ45       | Admin-Zugang                    |

## LED-Bedeutungen
| LED       | Farbe  | Bedeutung                             |
|-----------|--------|----------------------------------------|
| POWER     | Grün   | Gerät aktiv                            |
| STATUS    | Orange | Fehler oder Initialisierung läuft      |
| ALARM     | Rot    | Systemkritischer Fehler                |
| Port-LEDs | Grün   | Link-Up / Traffic                      |

## CLI-Befehle (FortiOS)
```cli
FGT100F login: admin
Password:

Welcome to FortiGate 100F
FGT100F #
FGT100F # config system interface
FGT100F (interface) # edit port1
FGT100F (port1) # set ip 192.0.2.1 255.255.255.0
FGT100F (port1) # set allowaccess ping https ssh
FGT100F (port1) # next
FGT100F (interface) # end
FGT100F # show firewall policy
FGT100F # diagnose hardware deviceinfo nic port1
FGT100F # execute reboot
Alarme & Fehlerszenarien
High CPU Load / RAM Exhaustion

Interface Down (port1 → no traffic)

Policy Mismatch → Blocked User Traffic

Session Limit erreicht (CGNAT overload)

VPN-Tunnel Down

Simulationseinfluss
simulate high-cpu → Delay für alle Policy-Entscheidungen

simulate interface-down port1 → Internetzugang bricht ab

simulate alarm-trigger → Systemstatus blinkt rot im Dashboard

simulate session-limit → aktive NAT-Sessions werden nicht mehr aufgebaut

YAML-Verknüpfung
yaml
Copy
Edit
id: firewall-fgt100f
type: Firewall
vendor: Fortinet
model: FortiGate 100F
ports:
  - name: port1
    role: WAN
    ip: 192.0.2.1/24
  - name: port2
    role: LAN
    ip: 10.0.0.1/24
status:
  cpu: 27
  sessions: 13924
  alarms: []
simulation_flags:
  - simulate high-cpu
  - simulate interface-down
  - simulate session-limit
✅ Mit dieser Komponente ist die Security-Schicht abgedeckt.
Sie lässt sich zwischen BRAS/NAT und dem Kundenverkehr platzieren, etwa für:

Session Enforcement

Deep Packet Inspection

CGNAT-Kopplung

VPN-Gateways