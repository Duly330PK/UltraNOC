📍 Beispiel: Privatkunde mit CGNAT in einem GPON-Netz
1. Backbone-Router (Core-Netz)
📡 Standort: Frankfurt am Main, DG-Kernknoten

🌐 Gerät: Nokia 7750 SR-C4 Core-Router

📡 IP: 185.57.192.1/30 (Interconnect zum Peering-Partner, z. B. DE-CIX)

🔁 Routing-Protokolle: BGP (Upstream), OSPF (intern), MPLS aktiv

Funktion:

Austausch von Routen mit dem globalen Internet via BGP (Upstreams & Peering)

Label Switching via MPLS für Verkehr zu/von BNG-Standorten

Default-Route für BNG: 0.0.0.0/0 via 185.57.192.2 label 1200

2. BNG (Broadband Network Gateway) – Aggregation Layer
📡 Standort: Köln Rechenzentrum

⚙️ Gerät: Nokia 7750 SR-12 BNG-Node

🔌 Uplink: MPLS over 10G zu Backbone (Core-Router)

🔐 DHCP Server für IPoE-Kunden

🌐 Öffentliche IPv4-Adresse für NAT: 91.194.84.73

💻 Beispielkunden-Verbindung:
Kunde mit privater IPv4 im Access-VLAN VLAN 2001, ONT MAC B8:27:EB:22:12:11

3. Access-Verbindung (OLT → ONT → Heimrouter)
🏠 Kunde: Max Mustermann, FTTH in Lüdinghausen, NRW

🔌 Technik: GPON (Passive Optical Network)

📡 ONT: Genexis Platinum 7840A

📦 Heimrouter: Fritz!Box 7530 AX (LAN-Port 1 → WAN des Routers)

📈 GPON-Struktur:
OLT-Port 1/2/1 → Splitter → 32 ONTs

VLAN: VLAN 2001 für ONT-Port 11

PON-ID: OLT1-PON1-ONT11

MAC-Adresse des ONT wird im OLT registriert (Line-ID)

Uplink vom OLT: 10G-Ethernet zum BNG Köln

📡 DHCP-Adressvergabe:
ONT/Router sendet DHCP Discover via VLAN 2001

BNG vergibt private IPv4: 100.72.15.212/30

Gateway (BNG-seitig): 100.72.15.213

DNS: 8.8.8.8, 8.8.4.4

DHCP-Lease-Time: 86400 s (24 h)

DHCP Option 82: PON-ID + OLT-Location zur Identifikation

4. NAT bei Deutsche Glasfaser (CGNAT)
📦 CGNAT-Konfiguration:
Eingehender Traffic:

Quell-IP: 100.72.15.212

Ziel-IP: 142.250.74.142 (google.com)

Quell-Port: 54133

Übersetzung auf öffentliche IP:

Öffentliche IPv4: 91.194.84.73

NAT-zugewiesener Port: 40965

CGNAT-Mapping:

100.72.15.212:54133 → 91.194.84.73:40965

Firewall-Policy erlaubt nur ausgehende Verbindungen

Portbereich pro Kunde: z. B. 40960–45055

5. Paketfluss – Beispiel DNS-Anfrage (IPv4)
Kunde gibt google.com im Browser ein.

DNS-Anfrage wird per IPv4 an 8.8.8.8 gesendet.

Fritz!Box leitet Anfrage über ONT ins VLAN 2001.

BNG empfängt Paket von 100.72.15.212, mapped auf 91.194.84.73:40965.

Core-Router sendet Paket an DE-CIX → Google.

Antwort von Google: 142.250.74.142 → 91.194.84.73:40965.

BNG findet Mapping, übersetzt zurück auf 100.72.15.212:54133.

ONT übergibt an Fritz!Box → Antwort im Browser.

6. Kunden-WAN-Ansicht
WAN-IP: 100.72.15.212

Öffentliche IP (sichtbar online): 91.194.84.73

NAT-Typ: „Symmetrisch“ (Test über STUN)

Portfreigabe: nicht möglich

IPv6: aktiviert, Prefix Delegation /56 → Fritz!Box verteilt lokal IPv6

7. NAT-Protokollierung intern
Logfile-Eintrag beim CGNAT-Gateway:

yaml
Copy
Edit
[2025-06-14T13:27:43Z] MAP: 100.72.15.212:54133 -> 91.194.84.73:40965
User-ID: PON1/ONT11@OLT1_LUEDINGHAUSEN
Lease: 86400s
📌 Zusatz: IPv6-Verhalten
Kunde erhält IPv6 Prefix: 2a0c:e640:ff00:3480::/56

WAN: 2a0c:e640:ff00:3480::1

Port-Forwarding über IPv6 möglich

Kein NAT auf IPv6 → direkter Zugriff auf Services

Fritz!Box setzt automatische Stateful Firewall: eingehend blockiert, freischaltbar