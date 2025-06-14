# UltraNOC – Änderungsprotokoll Updates 1–20

**Stand:** 2025-06-13  
**Projektverzeichnis:** `C:/noc_project/UltraNOC/`

---

## ✅ Update 1 – CLI API

**Datei:** `routers/cli.py`  
**Route:** `POST /api/v1/cli/send`  
**Funktion:** Simulierte Gerätekonsolen-Befehle

**PowerShell-Test:**
```powershell
$cmd = @{
  device = "router1"
  command = "show version"
} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/cli/send" -Method POST -Body $cmd -ContentType "application/json"
```

**Antwort (Beispiel):**
```json
{ "device": "router1", "output": "Simulierte Ausgabe für 'show version'" }
```

---

## ✅ Update 2 – Device API

**Datei:** `routers/devices.py`  
**Routen:** `GET`, `POST /api/v1/devices`

**PowerShell-Test (Eintrag):**
```powershell
$device = @{
  name = "router1"
  ip = "10.0.0.1"
  location = "Berlin"
} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/devices" -Method POST -Body $device -ContentType "application/json"
```

**Antwort:**
```json
{ "status": "added", "device": "router1" }
```

---

## ✅ Update 3 – Topologie API

**Datei:** `routers/topology.py`  
**Route:** `GET /api/v1/topology/map`

**PowerShell-Test:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/topology/map" -Method GET
```

**Antwort (Beispiel):**
```json
{ "nodes": [...], "links": [...] }
```

---

## ✅ Update 4 – Live Traffic API

**Datei:** `simulation/live_flow.py`  
**Route:** `POST /api/v1/simulation/live/pattern`

**PowerShell-Test:**
```powershell
$data = @{
  type = "burst"
  duration = 60
} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/simulation/live/pattern" -Method POST -Body $data -ContentType "application/json"
```

**Antwort:**
```json
{ "pattern": "burst", "status": "running" }
```

---

## ✅ Update 5 – Benutzerverwaltung

**Datei:** `routers/users.py`  
**Route:** `POST /api/v1/users`

**PowerShell-Test:**
```powershell
$user = @{
  username = "admin"
  email = "admin@example.com"
} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users" -Method POST -Body $user -ContentType "application/json"
```

**Antwort:**
```json
{ "status": "created", "username": "admin" }
```

---
