// Pfad: frontend/src/components/Widgets/AlarmPanel.jsx
import { useEffect, useState } from "react";

export default function AlarmPanel() {
  const [alarms, setAlarms] = useState([]);

  useEffect(() => {
    // Beispielhafte Alarme – später ersetzen durch API-Fetch
    const mockAlarms = [
      { device: "OLT Lüdinghausen", severity: "critical", msg: "GPON LOS detected" },
      { device: "BNG Köln", severity: "warning", msg: "High CPU usage" },
      { device: "ONT Max Mustermann", severity: "info", msg: "Session timeout" },
    ];
    setAlarms(mockAlarms);
  }, []);

  return (
    <div className="p-4 bg-white shadow-xl rounded-2xl w-full max-w-md">
      <h2 className="text-lg font-bold mb-4 text-red-600">Netzwerkalarme</h2>
      {alarms.length === 0 ? (
        <p className="text-sm text-gray-500">Keine aktiven Alarme</p>
      ) : (
        <ul className="text-sm list-disc ml-4">
          {alarms.map((alarm, index) => (
            <li
              key={index}
              className={
                alarm.severity === "critical"
                  ? "text-red-600"
                  : alarm.severity === "warning"
                  ? "text-yellow-600"
                  : "text-gray-600"
              }
            >
              <strong>{alarm.device}</strong>: [{alarm.severity.toUpperCase()}] {alarm.msg}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
