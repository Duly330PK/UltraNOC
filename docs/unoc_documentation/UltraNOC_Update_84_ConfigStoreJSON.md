📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 🗃️ UltraNOC – Update 84: config_store.json (Beispieldatei)

## 📂 Pfad

C:\noc_project\UltraNOC\data\config_store.json

yaml
Kopieren
Bearbeiten

---

## 📝 Zweck

Diese Datei dient als persistenter Speicher für Gerätekonfigurationen im JSON-Format. Sie wird vom Modul `config_store.py` gelesen und beschrieben.

---

## 📄 Beispielinhalt

```json
[
  {
    "device_id": "core-router-1",
    "config_data": "interface GigabitEthernet0/0\n description Uplink to ISP\n ip address 10.0.0.1 255.255.255.0"
  },
  {
    "device_id": "core-router-2",
    "config_data": "interface GigabitEthernet0/1\n description Backup Uplink\n ip address 10.0.1.1 255.255.255.0"
  }
]
🔒 Zugriff
Nur über die API-Routen store und load.

Änderungen außerhalb der API sollten vermieden werden.

🔧 Technische Hinweise
Die Datei muss im data/-Verzeichnis existieren oder wird automatisch erstellt.

Schreib-/Lesevorgänge erfolgen mit UTF-8-Codierung und JSON-Indentation (indent=2).

Kann später durch Datenbank oder Git-basiertes Versionierungssystem ersetzt werden.

© 2025 UltraNOC – JSON-basierte Gerätekonfigurationsablage