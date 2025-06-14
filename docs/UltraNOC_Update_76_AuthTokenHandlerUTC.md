📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 🔐 UltraNOC – Update 76: Token-Handler mit UTC-Zeit

## 📁 Betroffene Datei

- `backend/app/auth/token_handler.py`

---

## 🎯 Ziel

Die JWT-Token-Erstellung soll mit **UTC-basierten Zeitstempeln** erfolgen, um Konsistenz in Multizonen-Umgebungen, Auditing und Ablaufkontrollen zu gewährleisten.

---

## ⚙️ Änderungen

### 📝 Alt:
```python
from datetime import datetime, timedelta
expire = datetime.utcnow() + timedelta(...)
✅ Neu:
python
Kopieren
Bearbeiten
from datetime import datetime, timedelta, timezone
expire = datetime.now(timezone.utc) + timedelta(...)
🛡 Vorteile
Aspekt	Bewertung
Timezone-Awareness	✅
Sicherheit (Ablaufzeit)	✅
Kompatibilität	✅
CI/CD-Tauglichkeit	✅

🔧 Hinweise
Diese Änderung wirkt sich unmittelbar auf die Gültigkeitsdauer der JWT-Tokens aus.

Empfohlen wird auch die Verwendung einer UTC-kompatiblen Datenbankspalte für Token-Audit (später).

© 2025 UltraNOC – Sichere Authentifizierung auf globalem Zeitstandard