📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 🗂 UltraNOC – Config Store (Gerätekonfigurationen)

## 📌 Ziel
Ein persistenter Konfigurationsspeicher für Geräteeinstellungen. Speicherung im JSON-Format auf Dateisystemebene.

---

## 🔧 Architektur

| Komponente | Funktion |
|------------|----------|
| `routers/config_store.py` | API-Endpunkte zum Speichern/Abrufen |
| `data/config_store.json` | JSON-Datenspeicher |
| `main.py` | Router-Registrierung |

---

## 📁 Datei: routers/config_store.py

```python
@router.post("/store")
def store_config(entry: ConfigEntry):
    # Speichert Konfiguration unter device_id in JSON-Datei
python
Kopieren
Bearbeiten
@router.get("/load/{device_id}")
def load_config(device_id: str):
    # Lädt Konfiguration aus JSON-Datei
🧾 Datenmodell
python
Kopieren
Bearbeiten
class ConfigEntry(BaseModel):
    device_id: str
    config_data: str
💾 Beispiel – config_store.json
json
Kopieren
Bearbeiten
{
  "core-router-1": "interface Gig0/0\nip address 10.0.0.1 255.255.255.0",
  "core-router-2": "interface Gig0/1\nip address 10.0.1.1 255.255.255.0"
}
🔐 Sicherheit & Erweiterbarkeit
JSON-Datei ist systemseitig eingeschränkt

Spätere Anbindung an Datenbank möglich

GET-/POST-Endpunkte für Frontend & CLI-Schnittstellen geeignet

📡 API-Endpunkte:

Methode	Pfad	Beschreibung
POST	/api/v1/config/store	Konfiguration speichern
GET	/api/v1/config/load/{device_id}	Konfiguration abrufen

© 2025 UltraNOC – Config Store Modul (Stand: Update 60)