📄 Quelltext:

markdown
Kopieren
Bearbeiten
# 🧩 Update 63 – UTC-Anpassung im DeviceMetric-Datenmodell

## Zweck
Die Standard-Zeitstempelvergabe im SQLAlchemy-Modell `DeviceMetric` wurde aktualisiert. Ziel war die Ablösung der veralteten Methode `datetime.utcnow()` zugunsten einer zeitzonenbewussten, zukunftssicheren Lösung.

## Technischer Hintergrund
Python 3.12+ kennzeichnet `datetime.utcnow()` als deprecated. Empfohlen wird stattdessen die Nutzung von `datetime.now(timezone.utc)` für konsistente, UTC-basierte Zeitangaben.

## Datei
📄 `C:\noc_project\UltraNOC\backend\app\models\device_metrics.py`

## Änderung

### 🔧 Vorher
```python
from datetime import datetime
timestamp = Column(DateTime, default=datetime.utcnow)
✅ Nachher
python
Kopieren
Bearbeiten
from datetime import datetime, timezone
timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
Vorteile
🌐 Einheitliche Zeitbasis (UTC)

🔒 Kompatibel mit Auditing, Logging und Multi-Zonen-Betrieb

⚠️ Vermeidung künftiger Kompatibilitätswarnungen

🧪 Kein Migrationsaufwand erforderlich

Status
Bereich	Ergebnis
Funktionstest	✅ bestanden
Kompatibilität	✅ gegeben
Warnungsfreiheit	✅ erreicht