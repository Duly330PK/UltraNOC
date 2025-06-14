// Pfad: frontend/src/components/Widgets/MetricsPanel.jsx
import { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function MetricsPanel() {
  const [metrics, setMetrics] = useState([]);

  useEffect(() => {
    const interval = setInterval(() => {
      const timestamp = new Date().toLocaleTimeString();
      const newEntry = {
        time: timestamp,
        tx: Math.floor(Math.random() * 1000),
        rx: Math.floor(Math.random() * 1000),
        delay: parseFloat((Math.random() * 10).toFixed(2)),
        loss: parseFloat((Math.random() * 3).toFixed(2)),
      };
      setMetrics((prev) => [...prev.slice(-19), newEntry]);
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-4 bg-white shadow-xl rounded-2xl w-full max-w-2xl">
      <h2 className="text-lg font-bold mb-4 text-blue-600">Live-Metriken (global)</h2>

      <div className="mb-4">
        <h4 className="text-sm font-semibold">TX/RX Traffic</h4>
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={metrics}>
            <XAxis dataKey="time" hide />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="tx" stroke="#38bdf8" strokeWidth={2} dot={false} />
            <Line type="monotone" dataKey="rx" stroke="#34d399" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div>
        <h4 className="text-sm font-semibold">Delay / Packet Loss</h4>
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={metrics}>
            <XAxis dataKey="time" hide />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="delay" stroke="#facc15" strokeWidth={2} dot={false} />
            <Line type="monotone" dataKey="loss" stroke="#f87171" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}