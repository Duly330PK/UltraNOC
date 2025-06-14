📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 🕒 UltraNOC – Update 68: UTC-Zeitstandardisierung

## 📁 Pfad
C:\noc_project\UltraNOC\docs\UltraNOC_Update_68_UTC_Standardisierung.md

---

## 🎯 Ziel

Umstellung aller `datetime.utcnow()`-Aufrufe auf eine zeitzonenbewusste, zukunftssichere Variante:  
**`datetime.now(timezone.utc)`**  
Dies ermöglicht Kompatibilität mit Mehrzonen-Auswertung, Auditing und Zeitvergleichen.

---

## 🛠 Betroffene Dateien

| Datei                                             | Beschreibung                         |
|--------------------------------------------------|--------------------------------------|
| app\models\device_metrics.py                     | Default-Timestamp in DB-Modell       |
| app\routers\device_telemetry.py                  | Zeitstempel bei Push-Eintrag         |
| app\core\auth.py                                 | Token-Expiry-Berechnung              |

---

## ✅ Änderungen im Überblick

### 1. `device_metrics.py`

**Alt:**

```python
timestamp = Column(DateTime, default=datetime.utcnow)
Neu:

python
Kopieren
Bearbeiten
from datetime import timezone
timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
2. device_telemetry.py
Alt:

python
Kopieren
Bearbeiten
entry.timestamp = datetime.utcnow().isoformat()
Neu:

python
Kopieren
Bearbeiten
from datetime import timezone
entry.timestamp = datetime.now(timezone.utc).isoformat()
3. auth.py
Alt:

python
Kopieren
Bearbeiten
expire = datetime.utcnow() + timedelta(...)
Neu:

python
Kopieren
Bearbeiten
expire = datetime.now(timezone.utc) + timedelta(...)
🧪 Vorteil
Aspekt	Vorher (utcnow)	Nachher (timezone.utc)
Zeitzonenfähig	❌	✅
Kompatibel mit Audit	❌	✅
Zukunftssicher	⚠️ veraltet	✅
Pylance-Warnung	✅	❌

🛡 Empfehlung
Alle zukünftigen Zeitstempel (auch in neuen Modulen wie Logs, Sessions, Audits) sollten ausschließlich mit datetime.now(timezone.utc) erfolgen.

© 2025 UltraNOC – Zeitsysteme & Auditing