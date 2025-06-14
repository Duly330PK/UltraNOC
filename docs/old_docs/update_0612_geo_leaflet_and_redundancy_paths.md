
# UltraNOC – Änderungsbericht (Updates 6–12)

## 📦 Update 6: Fiber Types API

### 🔧 Pfad
`UltraNOC/backend/app/routers/fiber_types.py`

### 🧪 PowerShell-Test
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/fiber/types" -Method GET
```

### ✅ Ausgabe
```json
[
  "SMF",
  "MMF"
]
```

## 📦 Update 7: Network Quality API

### 🔧 Pfad
`UltraNOC/backend/app/routers/network_quality.py`

### 🧪 PowerShell-Test
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/network/quality" -Method GET
```

### ✅ Ausgabe
```json
{
  "latency": 12.3,
  "packet_loss": 0.1,
  "jitter": 2.1
}
```

## 📦 Update 8: Grafikexport (SVG)

### 🔧 Pfad
`UltraNOC/backend/app/routers/grafik_export.py`

### 🧪 PowerShell-Test
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/export/screenshot" -Method POST
```

### ✅ Ausgabe
```json
{
  "status": "created",
  "path": "export/map_<timestamp>.svg"
}
```

## 📦 Update 9: Audit Log API

### 🔧 Pfad
`UltraNOC/backend/app/routers/audit_log.py`

### 🧪 PowerShell-Test
```powershell
$entry = @{
  id = "1"
  username = "admin"
  action = "modify"
  target = "router1"
  timestamp = "2025-06-13T14:15:00"
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/audit/log" -Method POST -Body $entry -ContentType "application/json"
```

### ✅ Ausgabe
```json
{
  "id": "<uuid>",
  "username": "admin",
  "action": "modify",
  "target": "router1",
  "timestamp": "..."
}
```

## 📦 Update 10: VLANs API

### 🔧 Pfad
`UltraNOC/backend/app/routers/vlans.py`

### 🧪 PowerShell-Test
```powershell
$vlan = @{
  id = "1"
  vlan_id = 10
  name = "Mgmt"
  device = "sw1"
  timestamp = "2025-06-13T14:15:00"
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/vlans/add" -Method POST -Body $vlan -ContentType "application/json"
```

### ✅ Ausgabe
```json
{
  "id": "<uuid>",
  "vlan_id": 10,
  "name": "Mgmt",
  "device": "sw1",
  "timestamp": "..."
}
```

## 📦 Update 11: Session Tracking API

### 🔧 Pfad
`UltraNOC/backend/app/routers/session_data.py`

### 🧪 PowerShell-Test
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/sessions/create?user=admin&device=router1" -Method POST
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/sessions/active" -Method GET
```

### ✅ Ausgabe
```json
[
  {
    "id": "<uuid>",
    "user": "admin",
    "device": "router1",
    "start_time": "..."
  }
]
```

## 📦 Update 12: Preferences & Topology Metadata APIs

### 🔧 Pfade
- `UltraNOC/backend/app/routers/user_preferences.py`
- `UltraNOC/backend/app/routers/topology_meta.py`

### 🧪 PowerShell-Test
```powershell
$prefs = @{
  username = "admin"
  settings = @{ theme = "dark"; layout = "3D" }
} | ConvertTo-Json -Depth 3
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/preferences/save" -Method POST -Body $prefs -ContentType "application/json"

$meta = @{
  project = "UltraNOC Core"
  version = "1.0"
  regions = @("edge", "metro", "core")
} | ConvertTo-Json -Depth 3
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/topology/meta" -Method POST -Body $meta -ContentType "application/json"
```

### ✅ Ausgabe
```json
{ "status": "saved", "user": "admin" }
{ "status": "saved" }
```
