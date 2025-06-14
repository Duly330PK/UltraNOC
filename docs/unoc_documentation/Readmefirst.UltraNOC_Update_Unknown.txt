# UltraNOC – Path Metrics Feature (Update 70)

## 🎯 Zielsetzung
Einführung realistischer Metriken (Delay, Loss, Jitter) für jeden Link entlang eines Routingpfads, um:

- Pfadqualität sichtbar zu machen
- spätere Routingentscheidungen zu beeinflussen
- Simulationen dynamisch zu gestalten (bspw. bei Ausfallpfaden)

---

## 🧠 Backend – `path_metrics.py`

### 📍 Route
```http
GET /api/path/metrics/{source_id}/{target_id}
🔧 Funktion
Simuliert Delay-/Loss-/Jitter-Werte für vordefinierte Pfade

Gibt JSON zurück:

json
Copy
Edit
{
  "path": [
    {
      "from": "core1",
      "to": "bng1",
      "delay_ms": 3.52,
      "loss_percent": 0.05,
      "jitter_ms": 1.7,
      "timestamp": "2025-06-14T22:07:15.123Z"
    },
    ...
  ]
}
🔌 Frontend – Hook usePathMetrics.js
js
Copy
Edit
const { data, isLoading } = useQuery(
  ["pathMetrics", sourceId, targetId],
  () => axios.get(`/api/path/metrics/${sourceId}/${targetId}`).then((res) => res.data.path)
);
🎨 Darstellung – PathMetricsPanel.jsx
Visualisiert Metriken pro Hop

Farben: Grün (gut), Gelb (grenzwertig), Rot (schlecht)

Tooltip mit Details (Delay, Loss etc.)

🔁 Integration – TopologyView.jsx
Einbindung über <PathMetricsPanel pathMetrics={pathMetrics} />

Wird nur bei Auswahl eines Geräts aktiv

Kombiniert mit:

Redundanzpfad-Anzeige

Geräte-Metriken

Alarmanzeige

✅ Vorteile
Realistische Pfadbewertung auch ohne echte Telemetrie

Grundlage für:

Routing-Simulation (kürzester vs. stabilster Pfad)

Event-getriebene Ausfallsimulation

UI-Filter (z. B. nur stabile Pfade zeigen)

mathematica
Copy
Edit
