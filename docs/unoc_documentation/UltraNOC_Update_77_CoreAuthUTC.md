📄 Markdown-Quelltext:
markdown
Kopieren
Bearbeiten
# 🔐 UltraNOC – Update 77: UTC-Kompatibilität im Kernmodul auth.py

## 📁 Betroffene Datei

- `backend/app/core/auth.py`

---

## 🎯 Ziel

Konsistente JWT-Erzeugung und -Verifikation durch Verwendung von `datetime.now(timezone.utc)` statt des veralteten `datetime.utcnow()`.

---

## ⚙️ Änderungen

### 📝 Alt:
```python
expire = datetime.utcnow() + (expires_delta or timedelta(...))
✅ Neu:
python
Kopieren
Bearbeiten
expire = datetime.now(timezone.utc) + (expires_delta or timedelta(...))
🧪 Teststatus
Test	Ergebnis
Token erzeugen	✅
Token verifizieren	✅
Ablaufzeit korrekt UTC-basiert	✅

📝 Hinweise
Die jwt.decode()-Logik bleibt unverändert.

Gültigkeit wird anhand der UTC-exp-Angabe validiert.

Standardlaufzeit: 30 Minuten, wie in Konstante ACCESS_TOKEN_EXPIRE_MINUTES.

🔐 Sicherheit
Diese Umstellung verbessert nicht nur die Portabilität in Multi-Timezone-Setups, sondern ist auch eine Voraussetzung für zukünftige Features wie:

Token-Revocation

Session-Logging

Ablaufüberwachung mit Zeitzonenbezug

© 2025 UltraNOC – Zeitsichere Tokenverarbeitung im Auth-Core

perl
Kopieren
Bearbeiten
