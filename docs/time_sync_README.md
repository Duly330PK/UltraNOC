# Modul: Time Sync API

Dieses Modul bietet eine einfache Zeitabfrage-Schnittstelle für UltraNOC.

## Endpunkt

- **GET /api/v1/tools/time/current-time**

Antwort:

```json
{
  "time": "2025-06-13T16:00:00.000000",
  "timezone": "UTC"
}
```

## Zweck

Wird in zukünftigen Logs, grafischen Sessions, Playback-Streams und Telemetriedaten als Referenzzeit verwendet.

## Autor

UltraNOC DevOps
