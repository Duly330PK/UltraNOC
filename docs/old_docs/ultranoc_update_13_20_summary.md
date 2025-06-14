# UltraNOC – Update-Dokumentation (Updates 13–20)

## ✅ Update 13 – Sessions API

### Test 1: Session anlegen

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/sessions/create?user=admin&device=router1" -Method POST
```

**Antwort:**
```json
{
  "id": "bd3983f7-ed55-44f4-bb1b-1cc50abcc311",
  "user": "admin",
  "device": "router1",
  "start_time": "2025-06-13T12:22:39.498348"
}
```

### Test 2: Aktive Sessions anzeigen

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/sessions/active" -Method GET
```

---

## ✅ Update 14 – User Preferences API

### Test: Benutzerpräferenzen speichern

```powershell
$prefs = @{
  username = "admin"
  settings = @{ theme = "dark"; layout = "3D" }
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/preferences/save" -Method POST -Body $prefs -ContentType "application/json"
```

**Antwort:**
```json
{ "status": "saved", "user": "admin" }
```

---

## ✅ Update 15 – Topology Metadata API

### Test: Metadaten speichern

```powershell
$meta = @{
  project = "UltraNOC Core"
  version = "1.0"
  regions = @("edge", "metro", "core")
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/topology/meta" -Method POST -Body $meta -ContentType "application/json"
```

**Datei erzeugt:** `backend/data/topology_metadata.json`

**Inhalt:**
```json
{
  "regions": ["edge", "metro", "core"],
  "project": "UltraNOC Core",
  "version": "1.0"
}
```

---

## ✅ Update 16 – Fix: Verzeichnis automatisch anlegen

### Änderung:
Im Code von `topology_meta.py` wurde eingefügt:
```python
os.makedirs(os.path.dirname(TOPO_FILE), exist_ok=True)
```

---

## ✅ Update 17 – Maintenance Mode API

### Test: Wartungsmodus aktivieren

```powershell
$maint = @{ mode = "maintenance" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/maintenance/set" -Method POST -Body $maint -ContentType "application/json"
```

**Antwort:**
```json
{
  "mode": "maintenance",
  "since": "2025-06-13T12:53:00.061535"
}
```

---

## ✅ Update 18 – Alerting API

### Test: Alarm auslösen

```powershell
$alarm = @{
  source = "Router1"
  level = "critical"
  message = "CPU usage over 90%"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/alerts/raise" -Method POST -Body $alarm -ContentType "application/json"
```

---

## ✅ Update 19 – DNS Lookup API

### Test: DNS Lookup

```powershell
$dns = @{ hostname = "google.com" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/tools/dns/lookup" -Method POST -Body $dns -ContentType "application/json"
```

**Antwort:**
```json
{
  "hostname": "google.com",
  "ip": "64.233.184.139"
}
```

---

## ✅ Update 20 – Syslog Collector API

### Test: Syslog Nachricht senden

```powershell
$log = @{
  source = "Router1"
  severity = "warning"
  message = "Interface flapping"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/syslog/send" -Method POST -Body $log -ContentType "application/json"
```

**Antwort:**
```json
{
  "id": "96d11b5e-0b8c-46d3-987a-64c3976bfc59",
  "timestamp": "2025-06-13T12:58:47.535989",
  "source": "Router1",
  "severity": "warning",
  "message": "Interface flapping"
}
```

---
