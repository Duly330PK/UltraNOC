NEU:# Huawei EchoLife HG8245H – Optical Network Terminal (ONT)

## Überblick
- **Hersteller:** Huawei
- **Modell:** EchoLife HG8245H
- **Gerätetyp:** ONT (GPON Optical Network Terminal)
- **Einsatzbereich:** Endkundengerät für Glasfaseranschluss (FTTH)
- **Betriebssystem:** Huawei VRP Lite / proprietäre Embedded Firmware

---

## Ports & Interfaces

| Port        | Typ              | Beschreibung                         |
|-------------|------------------|--------------------------------------|
| PON         | SC/APC GPON      | Glasfaseranschluss vom OLT           |
| LAN1–LAN4   | Ethernet RJ-45   | Verbindung zu Endgeräten (CPE, PC)   |
| TEL1–TEL2   | RJ-11            | FXS Ports für VoIP-Telefonie         |
| USB         | USB 2.0 Host     | Für Medienfreigabe / LTE-Dongle      |
| POWER       | DC-In 12V        | Stromversorgung                      |
| RESET       | Button           | Werkseinstellungen wiederherstellen  |

---

## Physische Anzeigen (LEDs)

| LED          | Farbe  | Statusbedeutung                            |
|--------------|--------|---------------------------------------------|
| Power        | Grün   | Gerät ist eingeschaltet                     |
| PON          | Grün   | GPON-Verbindung aktiv                       |
| LOS          | Rot    | Kein Signal / Lichtverlust                  |
| Internet     | Grün   | Internetverbindung hergestellt              |
| WLAN         | Grün   | WLAN aktiv                                  |
| LAN1–4       | Grün   | Jeweilige LAN-Verbindung aktiv              |
| TEL1–2       | Grün   | Telefonverbindung aktiv                     |
| USB          | Grün   | USB-Gerät erkannt                           |

---

## CLI-Beispiele (telnet / debug-shell, Simulation)

```bash
HG8245H> enable
HG8245H# display wan-ip
WAN IP: 100.72.15.10
Subnet: 255.255.255.0
Gateway: 100.72.15.1

HG8245H# display pon-status
PON Status: Connected
RX Power: -23.7 dBm
TX Power: 2.1 dBm
OLT ID: 10.0.0.1
ONU ID: 1

HG8245H# display traffic lan1
Port: LAN1
RX: 245.1 MB
TX: 322.3 MB
Errors: 0

HG8245H# simulate fiber-break
[INFO] PON Link Down – LED LOS blinkt rot, Session lost
[ALARM] Optical Signal Loss Detected

HG8245H# reboot
Rebooting... Please wait.
Konfigurationsbeispiel
bash
Copy
Edit
HG8245H# configure terminal
HG8245H(config)# interface lan1
HG8245H(config-if)# ip address dhcp
HG8245H(config-if)# qos profile high
HG8245H(config-if)# exit
HG8245H(config)# wlan enable ssid "UltraNOC"
HG8245H(config)# save
Configuration saved.
Statusmetriken (Simulation)
Metrik	Einheit	Beispielwert
RX Power	dBm	-23.7
TX Power	dBm	2.1
Temperatur	°C	47
LAN1 Traffic	MB	322.3
VoIP Sessions	aktiv	1

Fehlerszenarien & Alarme
Zustand	Auswirkung
Optical Signal Loss	LED "LOS" blinkt, Internet offline, Alarm generiert
DHCP Timeout	Keine WAN-Adresse, kein Internet
High Temperature (>70 °C)	Alarm, Abschaltung nach 10 Min
Session Flood Detection	Alarm, evtl. Port Disable
Power Loss	Komplettausfall, Alarm auf OLT

Topologie-Integration
Verknüpft mit: Huawei MA5800-X17 (OLT) via PON

Typ: Endpunktknoten

Abhängigkeit: einseitig (abhängig von OLT)

Topologiedarstellung: Endgerät mit LED-Simulation

Sichtbar in Dashboard: JA (Status, TX/RX, Alarm)

Simulationseinfluss
Fiber Break: Unterbricht PON → erzeugt "LOS"

Session Flood: Löst Warnung aus, Simuliert DoS

Power Loss: Kompletter Node-Failure

Restart: Zeigt Bootphase, LEDs sequentiell aktiv

CLI-Eingaben: Ändern Statuswerte und Sessions live

Besonderheiten
Unterstützt PPPoE, DHCP, VLAN Tagging

NAT/PAT via CPE-Funktionalität (optionale Simulation)

FEC, Layer 2 Isolation, MAC Filtering konfigurierbar

WebGUI ebenfalls simuliert (perspektivisch)

Hinweise zur Simulation
Device wird regelmäßig via poll_metrics überwacht

LED-Status wirkt sich auf Dashboard + TopoMap aus

CLI-Kommandos triggern device_state-Änderung in Store

Fehlerstatus erzeugt Einträge im Alarmlog (mit Timestamp)

Fazit
Der HG8245H bildet die Endkundenseite eines realistischen FTTH-Szenarios ab. Er liefert wichtige Edge-Zustände, Alarmierungen und Session-Statistiken, um Servicequalität und Redundanz auf Access-Ebene zu analysieren. Durch CLI- und LED-Integration ist das Gerät vollumfänglich simuliert.

yaml
Copy
Edit
ALT:
# Huawei EchoLife HG8245H – ONT (Optical Network Terminal)

## Überblick
- Hersteller: Huawei
- Modell: EchoLife HG8245H
- OS: Huawei Embedded (WebUI + TR-069 + Telnet-CLI)
- Einsatz: Kunden-ONT, Abschlussstelle der Glasfaserleitung

## Physische Eigenschaften
| Merkmal           | Beschreibung                                      |
|------------------|---------------------------------------------------|
| LEDs              | PON, LOS, POWER, INTERNET, LAN1–LAN4, WLAN, TEL1 |
| Gehäuse           | Weiß, Tischgerät, Wandmontage möglich            |
| Anschlüsse        | 4x RJ45 LAN, 2x TEL (RJ11), 1x SC/APC             |
| Management        | Webinterface (192.168.100.1), TR-069, Telnet     |

## Portübersicht
| Port     | Typ        | Funktion                         |
|----------|------------|----------------------------------|
| SC/APC   | Optisch    | Glasfaseranschluss zum OLT       |
| LAN1–4   | RJ45       | Ethernet-Ausgänge für Geräte     |
| TEL1–2   | RJ11       | Analog-Telefonanschlüsse         |
| WLAN     | Intern     | 2.4 GHz / 5 GHz WLAN              |

## LED-Bedeutungen
| LED     | Farbe   | Bedeutung                         |
|---------|---------|------------------------------------|
| POWER   | Grün    | Gerät eingeschaltet                |
| LOS     | Rot     | Kein optisches Signal              |
| PON     | Grün    | Verbindung aktiv                   |
| INTERNET| Grün    | IP-Adresse erhalten                |
| WLAN    | Grün    | WLAN aktiv                         |
| LANx    | Gelb    | Port aktiv                         |

## Simulierbare Szenarien
- **LOS Error** (PON blinkt, LOS rot) bei Glasfaserbruch
- **IP-Konflikt** (keine Internet-LED, DHCP-Failure)
- **Reset gedrückt** → Neustart + Re-Provisionierung via TR-069
- **PPPoE-Ausfall** → Kein Internet trotz PON grün
- **WLAN-Ausfall** → Kein SSID Broadcast

## Simulationseinflüsse
- `simulate fiber-break` → OLT erkennt ONT als offline
- `simulate reboot` → alle LEDs aus, dann langsames Hochfahren
- `simulate dhcp_conflict` → PON aktiv, aber kein Internet
- Keine CLI-Steuerung – Konfiguration via OLT / ACS

## YAML-Verknüpfung
```yaml
id: ont-huawei-hg8245h
type: ONT
vendor: Huawei
model: HG8245H
connection: gpon0/1/3 → olt-ma5800-x17
status:
  pon: up
  internet: down
  los: false
  leds:
    - name: PON
      color: green
    - name: LOS
      color: off
    - name: INTERNET
      color: off
simulation_flags:
  - simulate fiber-break
  - simulate reboot
