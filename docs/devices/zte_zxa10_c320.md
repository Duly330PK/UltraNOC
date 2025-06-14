# ZTE ZXA10 C320 – Compact OLT

## Überblick
- Hersteller: ZTE
- Modell: ZXA10 C320
- OS: ZTE OLT Firmware (CLI-ähnlich ZTE OLT VRP)
- Einsatz: GPON-OLT für Fiber-to-the-Home (FTTH) Netze

## Physikalische Merkmale
- Bauhöhe: 2U, rackmountfähig
- Gewicht: ca. 6.5 kg
- Stromversorgung: 220 V AC oder 48 V DC, je nach Netzteilmodul
- Lüfter: 2 redundante Module
- LEDs:
  - **PWR** (Power): grün/rot
  - **RUN** (Systemstatus): blinkend grün
  - **ALM** (Alarm): rot bei Fehler
  - **PON/LOS** pro Port
- Zugriff:
  - Konsole: RJ45 oder USB serial
  - Management: ETH MGMT-Port (10/100Base-T)

## Ports & Interfaces

| Port     | Typ               | Beschreibung              |
|----------|------------------|---------------------------|
| gpon0/1  | GPON Port         | Fiber-Anschluss für ONTs |
| eth0     | Ethernet (Mgmt)   | Management-Zugang         |
| cons     | Serial Console    | Lokaler CLI-Zugriff       |

## CLI-Beispiele

```cli
ZTE> enable
ZTE# configure terminal
ZTE(config)# interface gpon-olt_1/1
ZTE(config-if)# onu 1 type ZTE-F660 sn ZTEG12345678
ZTE(config-if)# exit
ZTE(config)# service-port 1 vlan 100 gpon 1/1/1 ont 1 gemport 1 multi-service user-vlan 100 tag-transform translate
ZTE(config)# interface vlan 100
ZTE(config-if)# ip address 192.168.1.1 255.255.255.0
ZTE(config-if)# no shutdown
Alarm- und Fehlerszenarien
❗ LOS (Loss of Signal): LED blinkt rot, show alarm active zeigt:

cli
Copy
Edit
ZTE# show alarm active
1: OLT GPON1/1/1: LOS Alarm - No signal from ONT
❗ High Temperature:

cli
Copy
Edit
ZTE# show environment
FAN 1: OK
FAN 2: OK
TEMP: 72°C (Warning Threshold: 70°C)
❗ ONT Offline:

cli
Copy
Edit
ZTE# show onu status gpon-olt_1/1
ONU 1: DOWN – Last Seen: 08:42:12
Simulationseinfluss (UltraNOC)
Simulation	Reaktion im Gerät
simulate fiber-break	PON-LOS, Alarmmeldung, ONT offline
simulate reboot	Neustart CLI, temporärer Trafficverlust
simulate overload	CPU-Warnung, Alarmtemperatur

Statusfelder & Metriken
Metrik	Einheit	Beispielwert
RX Power	dBm	–18.4
TX Power	dBm	2.5
CPU Load	%	45
Temperatur	°C	58
Fan Speed	RPM	4200

Konfigurationsauszug
cli
Copy
Edit
vlan 100 smart
  port gpon-olt_1/1/1
  port eth0
  name FTTH_VLAN
!
interface vlan 100
  ip address 192.168.1.1 255.255.255.0
!
gpon-onu_1/1/1:1
  sn-bind enable
  native-vlan 100
!
Verknüpfungen
Direkt verbunden mit Patchpanel GPON-Panel 1 (Slot 1/1)

ONT HG8245H an Port gpon1/1/1

Management über eth0 via VLAN 10

Besondere Funktionen
FEC aktiviert pro Port (optional deaktivierbar)

VLAN-Stacking möglich

PPPoE passthrough fähig

SNMPv2 für Monitoring