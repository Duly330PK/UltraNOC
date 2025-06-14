📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 📊 UltraNOC – Update 75: UTC-Zeitstempel für Device-Metriken

## 📁 Betroffene Datei

- `backend/app/models/device_metrics.py`

---

## 🎯 Ziel

Standardisierung aller gespeicherten Zeitstempel auf UTC. Dies ist essenziell für eine saubere Verarbeitung und Korrelation in Metrikdatenbanken und Dashboards.

---

## ⚙️ Änderungen

### 📝 Alt:
```python
from datetime import datetime
timestamp = Column(DateTime, default=datetime.utcnow)
✅ Neu:
python
Kopieren
Bearbeiten
from datetime import datetime, timezone
timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
📌 Erklärung
datetime.utcnow ist deprecated (nicht timezone-aware).

datetime.now(timezone.utc) erzeugt timezone-aware datetime-Objekte.

Lambda notwendig, um bei SQLAlchemy Callable als Default zu setzen.

✅ Ergebnisse
Feature	Status
UTC-Zeitzone aktiv	✅
Pydantic-Kompatibilität	✅
ORM-Konformität	✅

© 2025 UltraNOC – Konsistente Zeitführung in der Metrikerfassung