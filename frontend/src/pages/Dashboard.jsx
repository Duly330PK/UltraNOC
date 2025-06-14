// C:\noc_project\UltraNOC\frontend\src\pages\Dashboard.jsx

import React from "react";
import ClockWidget from "../components/Widgets/ClockWidget";

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <h1 className="text-3xl font-bold mb-6">Welcome to UltraNOC</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <ClockWidget />
        {/* Weitere Widgets folgen */}
      </div>
    </div>
  );
}
