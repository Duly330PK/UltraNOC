// frontend/src/components/Map/CableInfoPanel.jsx
import React from "react";

export default function CableInfoPanel({ link }) {
  if (!link || typeof link !== "object") return null;

  const {
    id = "unbekannt",
    type = "unbekannt",
    length = "–",
    db_loss = "–",
    status = "unknown"
  } = link;

  const statusColor =
    status === "up"
      ? "text-green-600"
      : status === "down"
      ? "text-red-600"
      : "text-gray-600";

  return (
    <div className="absolute left-4 bottom-20 bg-white text-black p-4 rounded shadow z-20 w-80">
      <h3 className="font-bold mb-2">Leitungsinfo</h3>
      <p><strong>ID:</strong> {id}</p>
      <p><strong>Typ:</strong> {type}</p>
      <p><strong>Länge:</strong> {length} m</p>
      <p><strong>dB-Verlust:</strong> {db_loss} dB</p>
      <p>
        <strong>Status:</strong>{" "}
        <span className={`${statusColor} font-bold`}>
          {status}
        </span>
      </p>
    </div>
  );
}
