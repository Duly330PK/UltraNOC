// frontend/src/components/Map/PathMetricsPanel.jsx
import React from "react";

export default function PathMetricsPanel({ pathMetrics }) {
  const safeMetrics = Array.isArray(pathMetrics) ? pathMetrics : [];

 const getColor = (delay) => {
    if (delay < 5) return "bg-green-500";
    if (delay < 10) return "bg-yellow-500";
    return "bg-red-500";
  };

  return (
    <div className="absolute left-4 bottom-20 bg-white text-black p-4 rounded shadow z-20 w-96">
      <h3 className="text-lg font-bold mb-3">Pfadmetriken</h3>
      <ul className="space-y-2 text-sm">
        {pathMetrics.map((link, idx) => (
          <li key={idx} className="flex justify-between items-center">
            <div>
              <span className="font-medium">
                {link.source} → {link.target}
              </span>
              <div className="text-xs text-gray-500">
                {link.hops} hops – {link.loss}% Verlust
              </div>
            </div>
            <div className={`w-16 text-center py-1 rounded text-white ${getColor(link.delay)}`}>
              {link.delay} ms
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
