
# 🧠 UltraNOC Update 56 – Snapshot Handler API

Dieses Modul erweitert das Backend um die Fähigkeit, Gerätestände oder Netzwerktopologien als Snapshots abzulegen oder wiederherzustellen.

## ✨ Enthaltene Features:
- POST `/api/v1/snapshots/save` – Speichert aktuellen Zustand (Mock-Version)
- GET `/api/v1/snapshots/load/{id}` – Lädt gespeicherten Snapshot
- In-Memory-Speicherung (kann später auf DB/Festplatte erweitert werden)

## 📁 Zielpfad
```
UltraNOC/backend/app/routers/snapshot_handler.py
```

## 🧪 Status
Manuell getestet via PowerShell und HTTPie. Persistenz folgt in Update 57.
