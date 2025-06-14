Hier ist eine konkrete Beispiel-Route mit IPs, die den kompletten Pfad einer IP-Verbindung in einem typischen FTTH-Netz mit CGNAT zeigt – mit besonderem Fokus darauf, wie eine IP forensisch eindeutig identifiziert werden kann.

🧭 Ziel: Route einer IP-Verbindung im CGNAT-Netz bis zum Kunden
🌐 Startpunkt: Webserver / Opferseite
🔍 Erkennt:

yaml
Copy
Edit
Verbindung von: 91.194.84.73:40965
Zeit: 2025-06-14 13:27:43 UTC
Protokoll: TCP
Ziel: 443 (HTTPS)
💡 → Die Server-Logs enthalten:

Öffentliche IP-Adresse (vom CGNAT)

Port, der vom Carrier-NAT vergeben wurde

Zeitstempel

Ziel-Port (443 → HTTPS)

🚀 Route durch das Netz (vereinfacht als Hop-by-Hop)
Hop	Gerät (Netzebene)	Funktion	IP-Adressen
1	Webserver	Zielsystem	185.60.216.35
2	Internet/Peering	Weiterleitung über DE-CIX etc.	—
3	Core-Router (DG, Frankfurt)	Border-Router, BGP/MPLS	ASN: 60294, 185.57.192.1/30
4	Backbone DG	MPLS-Netzwerk, Label Switching	MPLS Labels: z. B. Label 1200
5	BNG (Köln)	NAT, DHCP, Routing	🔸 NAT-IP: 91.194.84.73
🔸 Kunde: 100.72.15.212
6	Aggregation-Switch	VLAN/QinQ Tunnel	VLAN 2001
7	OLT (Lüdinghausen)	PON-Termination	GPON-ID: OLT1-PON1-ONT11
8	ONT	Ethernet-Konvertierung	WAN-IP: 100.72.15.212
9	Fritzbox (Kunde)	Heimnetz-NAT	LAN: 192.168.178.0/24, z. B. 192.168.178.22

🔍 Forensische Auflösung (Rückverfolgung der IP)
Ermittler haben:

IP: 91.194.84.73

Port: 40965

Zeit: 2025-06-14 13:27:43 UTC

Protokoll: TCP

🔁 Provider (Deutsche Glasfaser) durchsucht CGNAT-Logfiles nach diesem Mapping:

log
Copy
Edit
[2025-06-14T13:27:43Z] NAT MAP:
External: 91.194.84.73:40965
→ Internal: 100.72.15.212:54133
Protocol: TCP
OLT/ONT: OLT1-PON1-ONT11
MAC: B8:27:EB:22:12:11
UserID: DGF-NRW-2025-4558
📌 Rückverfolgungskette:

mathematica
Copy
Edit
IP 91.194.84.73:40965 (öffentlich)
↓ (via NAT Log)
IP 100.72.15.212:54133 (Kundenseitig)
↓ (via DHCP Log)
MAC B8:27:EB:22:12:11 → Fritzbox
↓
ONT Port 11 am OLT1, Lüdinghausen
↓
Kunde Max Mustermann, Musterstraße 1
✅ Ergebnis: Eindeutige Identifikation
Zum Zeitpunkt 2025-06-14 13:27:43Z hat der Kunde
Max Mustermann, Anschluss-Nr. DGF-NRW-2025-4558,
hinter CGNAT-IP 91.194.84.73:40965
mit der internen IP 100.72.15.212:54133
eine Verbindung aufgebaut.

📦 Zusammenfassung der Route mit IPs
text
Copy
Edit
Client (LAN):         192.168.178.22:52634
→ Fritzbox NAT
→ WAN IP:             100.72.15.212:54133
→ CGNAT (BNG):        91.194.84.73:40965
→ Internet Backbone:  via MPLS → BGP
→ Zielserver:         185.60.216.35:443 (HTTPS)