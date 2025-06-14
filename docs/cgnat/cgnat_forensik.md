🧭 Ziel: Nutzer hinter CGNAT identifizieren
🔍 Problem:
Viele Kunden teilen sich eine öffentliche IPv4-Adresse (z. B. 91.194.84.73).
→ Es reicht nicht, nur die IP zu kennen.
→ Man muss auch den genauen Zeitstempel und den Port kennen, den der Nutzer genutzt hat.

✅ Voraussetzungen für eindeutige forensische Zuordnung
Parameter	Beschreibung
🌍 Öffentliche IP-Adresse	z. B. 91.194.84.73 (CGNAT-Adresse des Providers)
⏱️ Exakter Zeitstempel	z. B. 2025-06-14 13:27:43 UTC (am besten auf Sekunden genau)
🔌 Zielport (TCP/UDP)	z. B. 40965 – der vom CGNAT zugewiesene Port
📡 Protokolltyp	TCP oder UDP (z. B. HTTP = TCP/80, DNS = UDP/53)

📂 Schritt-für-Schritt: CGNAT-Forensik – Zuordnung
1. Logging durch den Zielserver (oder Ermittler)
Ein Webdienst, FTP-Server oder anderer Dienst loggt eingehende Verbindungen mit:

log
Copy
Edit
[2025-06-14T13:27:43Z] CONNECT from 91.194.84.73:40965 → TCP
Diese IP + Port + Zeitangabe ist essenziell.

2. Gerichtlicher Auskunftsersuch an den Provider (z. B. Deutsche Glasfaser)
Die Ermittlungsbehörden übermitteln:

Öffentliche IP: 91.194.84.73

Zielport: 40965

Zeitpunkt: 2025-06-14 13:27:43 UTC

Protokoll: TCP

Rechtsgrundlage: z. B. § 113b TKG in Kombination mit § 100g StPO (Telekommunikationsüberwachung)

3. Provider-Auswertung: CGNAT-Session-Logs
Deutsche Glasfaser oder ein anderer ISP führt interne Session-Logs im CGNAT-Gateway:

log
Copy
Edit
MAP: 100.72.15.212:54133 → 91.194.84.73:40965
PON-ID: OLT1-PON1-ONT11
User-Contract-ID: DGF-NRW-2025-4558
LeaseStart: 2025-06-14T13:27:40Z
LeaseEnd: 2025-06-14T13:57:40Z
➡️ Der Provider kann nun anhand der NAT-Tabelle und Logs feststellen:

Feld	Wert
Interne IP	100.72.15.212
Kunde	Max Mustermann, Musterstraße 1
Vertrag	DGF-NRW-2025-4558
Anschluss	ONT ID: OLT1-PON1-ONT11
WAN MAC	B8:27:EB:22:12:11 (Fritzbox)

4. Ergebnis: Klare Nutzer-Zuordnung
✅ Der Betreiber kann nun gerichtsfest sagen:
„Zum Zeitpunkt 2025-06-14T13:27:43Z nutzte der Kunde Max Mustermann, wohnhaft in Lüdinghausen, den Port 40965 der öffentlichen IP 91.194.84.73.“

Diese Zuordnung ist in Deutschland zulässig und wird in Ermittlungen regelmäßig verwendet (z. B. Urheberrechtsverletzungen, Bedrohungen, Betrug).

🛡️ Datenschutzrechtliche Rahmen
TKG § 174 ff. regelt Verpflichtung zum Logging.

Der Provider muss Port- und Zeitbezogene Zuordnung speichern – meist für 7 bis 14 Tage.

Zugriff nur bei rechtlicher Anordnung (Richter oder Staatsanwalt).

Logging erfolgt nicht pauschal, sondern gezielt für NAT-Mapping (nicht Surfverhalten).

🧪 Beispielhafte NAT-Zuordnung in einem Carrier-NAT-System
Externe Sicht	CGNAT-Gateway intern	Kundenseite
91.194.84.73:40965	→ 100.72.15.212:54133	Fritzbox hinter ONT
Zeit: 13:27:43Z	+ Protokoll: TCP	IP intern per DHCP erhalten
Ziel: z. B. google.com	Session gehalten bis 13:57:40Z	

❗ Sonderfall: Fehlen des Ports
🔻 Wenn der Zielserver nur die öffentliche IP loggt (ohne Port), ist keine eindeutige Zuordnung möglich.

Denn: 200 Nutzer könnten gleichzeitig 91.194.84.73 verwenden – der Port ist das einzige Unterscheidungsmerkmal.

📌 Fazit: Was braucht man für Forensik bei CGNAT?
Benötigt	Warum?
✅ Öffentliche IP	Identifiziert CGNAT-Adresse
✅ Exakter Zeitstempel	Session-Lookup
✅ Zielport + Protokoll	Eindeutige Zuordnung im NAT
❌ Nur IP?	Nicht eindeutig (geteilt)