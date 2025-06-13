# UltraNOC – Änderungsprotokoll Updates 21–50

**Stand:** 2025-06-13  
**Projektverzeichnis:** `C:/noc_project/UltraNOC/`

---

## ✅ Update 21 – Kabeldiagnose API

**Datei:** `routers/cable_diagnostics.py`  
**Routen:** `POST /diagnostics/run`, `POST /diagnostics/diagnose`  
**Funktion:** Simuliert Leitungstest & Fehlerbewertung  

**PowerShell-Test:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/cables/diagnostics/run" -Method POST
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/cables/diagnostics/diagnose" -Method POST
```

---

## ✅ Update 22 – IPv6 Validator

**Datei:** `routers/ipv6_tools.py`  
**Route:** `POST /api/v1/tools/ipv6/analyze`  

**PowerShell-Test:**
```powershell
$ipv6 = @{ address = "2001:db8::1" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/tools/ipv6/analyze" -Method POST -Body $ipv6 -ContentType "application/json"
```

---

## ✅ Update 23 – Ereignis-Trigger

**Datei:** `routers/event_trigger.py`  
**Routen:** `POST /trigger`, `GET /triggered`  

**PowerShell-Test:**
```powershell
$event = @{ source = "UPS1"; event_type = "battery"; detail = "Voltage drop detected" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/events/trigger" -Method POST -Body $event -ContentType "application/json"
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/events/triggered" -Method GET
```

---

## ✅ Update 24 – Gerätegesundheit

**Datei:** `routers/device_health.py`  
**Routen:** `POST /report`, `GET /latest`  

**PowerShell-Test:**
```powershell
$health = @{ device = "RouterX"; cpu_usage = 65.4; memory_usage = 72.1 } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/devices/health/report" -Method POST -Body $health -ContentType "application/json"
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/devices/health/status" -Method GET
```

---

## ✅ Update 25 – Zeitplanung

**Datei:** `routers/scheduled_tasks.py`  
**Routen:** `POST /add`, `GET /list`  

**PowerShell-Test:**
```powershell
$task = @{ task = "Backup DB"; run_at = "2025-06-14T02:00:00" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/scheduler/add" -Method POST -Body $task -ContentType "application/json"
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/scheduler/list" -Method GET
```

---

## ✅ Update 26 – Vorfallsmeldung

**Datei:** `routers/incidents.py`  
**Routen:** `POST /raise`, `GET /all`  

**PowerShell-Test:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/incidents/raise?source=Node5&impact=link_failure" -Method POST
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/incidents/summary" -Method GET
```

---

## ✅ Update 27 – Inventory YAML Support

**Datei:** `routers/inventory.py`  
**Route:** `GET /inventory/list`  
**Ablage:** `data/devices.yml` (Beispiel siehe unten)

```yaml
- name: Switch1
  model: Catalyst
- name: RouterX
  model: Juniper
```

---

## ✅ Update 28 – Test Suite Automation

**Datei:** `run_all_tests.ps1`  
**Funktion:** Führt alle `pytest`-basierten Tests nacheinander aus  
**Statusausgabe:** Jeder Test mit ✅/❌ markiert

---

## ✅ Update 29 – Einheitliche API-Namensräume

Alle Routen wurden unter `/api/v1/` strukturiert (z. B. `/tools`, `/devices`, `/events`, `/scheduler`)

---

## ✅ Update 30–49 – Refactoring & Stabilisierung

- Standardisierung der Responses (`target`, `status`, `error`)
- Alle APIs testbar mit PowerShell und pytest
- Fehlerbehandlung vereinheitlicht (z. B. Rückgabe von `"status": "error"` bei Exception)

---

## ✅ Update 50 – Ping Tool Konsistenzpatch

**Datei:** `routers/ping_tool.py`  
**Route:** `POST /api/v1/tools/ping`  

**Neues Verhalten:**  
Antwort enthält immer `target`, `status`, und `output`/`error`:

```json
{
  "target": "192.0.2.1",
  "status": "failed",
  "error": "Host unreachable"
}
```

**PowerShell-Test:**
```powershell
$ping = @{ target = "192.0.2.1" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/tools/ping" -Method POST -Body $ping -ContentType "application/json"
```

**Testdatei:** `tests/test_ping_tool.py`  
✅ Test erfolgreich nach Patch

---