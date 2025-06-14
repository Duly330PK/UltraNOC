// C:\noc_project\UltraNOC\frontend\src\components\devices\DeviceCard.jsx

import React from "react";

const DeviceCard = ({ name, type, status, location }) => {
  const statusColor = status === "online" ? "bg-green-500" : "bg-red-500";

  return (
    <div className="bg-gray-800 rounded shadow p-4 w-64 text-white flex flex-col gap-2">
      <div className="flex justify-between items-center">
        <h2 className="text-lg font-semibold">{name}</h2>
        <span className={`w-3 h-3 rounded-full ${statusColor}`} title={status}></span>
      </div>
      <div className="text-sm text-gray-300">{type}</div>
      <div className="text-xs text-gray-400">📍 {location}</div>
      <div className="mt-2 flex gap-2">
        <button className="bg-nocblue hover:bg-blue-700 px-3 py-1 rounded text-xs">
          CLI öffnen
        </button>
        <button className="bg-gray-700 hover:bg-gray-600 px-3 py-1 rounded text-xs">
          Details
        </button>
      </div>
    </div>
  );
};

export default DeviceCard;
