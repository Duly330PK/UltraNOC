📄 UltraNOC_Update_63_UTC_Timestamping.md
🔽 Download ZIP (1 Datei)

markdown
Kopieren
Bearbeiten
# Update 63 – UTC-Zeitstempelung vereinheitlicht (UltraNOC)

## Ziel
Konsistente Nutzung von UTC-Zeitstempeln in allen Modulen zur Unterstützung von Auditing, Multi-Zonen-Kompatibilität und künftiger Korrelation mit externen Systemen.

---

## 🧭 Betroffene Dateien & Änderungen

### 1. `device_telemetry.py`

**Pfad:** `C:\noc_project\UltraNOC\backend\app\routers\device_telemetry.py`

**Änderung:**
```diff
- entry.timestamp = datetime.utcnow().isoformat()
+ entry.timestamp = datetime.now(timezone.utc).isoformat()
2. device_metrics.py
Pfad: C:\noc_project\UltraNOC\backend\app\models\device_metrics.py

Änderung:

diff
Kopieren
Bearbeiten
- timestamp = Column(DateTime, default=datetime.utcnow)
+ timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
3. auth.py
Pfad: C:\noc_project\UltraNOC\backend\app\core\auth.py

Änderung:

diff
Kopieren
Bearbeiten
- expire = datetime.utcnow() + ...
+ expire = datetime.now(timezone.utc) + ...
📌 Hintergrund
Die Methode datetime.utcnow() ist deprecated in Pylance/Python ≥3.12.

Künftig wird ausschließlich datetime.now(timezone.utc) verwendet.

Kompatibel mit FastAPI, SQLAlchemy, JWT und Pydantic.

✅ Ergebnis
Komponente	Status
UTC-Zeit in Telemetrie	✅ Aktiv
UTC-Zeit in Device Metrics	✅ Aktiv
UTC-Zeit für Token-Expiry	✅ Aktiv
Zukunftssicherheit (Pylance)	✅ Gewährleistet
