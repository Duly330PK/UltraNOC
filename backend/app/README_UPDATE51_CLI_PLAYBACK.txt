📄 Update 51 – CLI Playback Integration

✅ Betroffene Datei:
- UltraNOC/backend/app/routers/cli_playback.py

🔧 Eingebundener Endpunkt:
GET /api/v1/playback/{session_id}

📦 Rückgabeformat (standardisiert mit ResponseModel):
{
  "session_id": "abc-123",
  "commands": [
    {"timestamp": "2025-06-13T10:00:00", "command": "show ip interface brief"},
    {"timestamp": "2025-06-13T10:00:05", "command": "show version"}
  ]
}

⚙️ Hinweis:
Der Router ist in UltraNOC/backend/app/main.py bereits eingebunden unter:
app.include_router(cli_playback.router, prefix="/api/v1/playback", tags=["CLI Playback"])
