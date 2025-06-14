📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 🗂 UltraNOC – Config Store API

## 📌 Ziel
Persistente Speicherung und Abruf von Gerätekonfigurationen (z. B. CLI, Templates) in einem JSON-basierten Store.

---

## 📦 Komponenten

| Pfad | Funktion |
|------|----------|
| `routers/config_store.py` | API-Router zur Konfig-Verwaltung |
| `data/config_store.json` | JSON-Speicher der Konfigurationen |

---

## 🧩 Datenmodell (Pydantic)

```python
class ConfigEntry(BaseModel):
    device_id: str
    config_data: str
→ JSON wird durch Gerät-ID indiziert.

📤 Endpunkte
Methode	Pfad	Beschreibung
POST	/api/v1/config/store	Konfiguration speichern
GET	/api/v1/config/load/{device_id}	Konfiguration abrufen

💾 Beispielinhalt (data/config_store.json)
json
Kopieren
Bearbeiten
{
  "core-router-1": "interface GigabitEthernet0/0\n description Uplink to ISP\n ip address 10.0.0.1 255.255.255.0",
  "core-router-2": "interface GigabitEthernet0/1\n description Backup Uplink\n ip address 10.0.1.1 255.255.255.0"
}
🔐 Sicherheit
Aktuell ohne Auth-Absicherung – später durch Rollenfilter erweiterbar (z. B. „engineer“ / „admin“).

📦 Zusammenfassung
Vorteil	Beschreibung
✅	Lokaler JSON-Speicher ohne Datenbankbelastung
✅	Schneller Zugriff durch Schlüsselzuweisung
🛠	Erweiterbar für UI-Editing, Snapshots, Versionshistorie

© 2025 UltraNOC – Config Store (Update 60)