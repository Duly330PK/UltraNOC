// C:\noc_project\UltraNOC\frontend\src\pages\DashboardPage.jsx

import React from "react";
import ClockWidget from "../components/Widgets/ClockWidget";

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <h1 className="text-3xl font-bold mb-6">🔧 UltraNOC Dashboard</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        <ClockWidget />
        {/* Weitere Widgets folgen hier */}
      </div>
    </div>
  );
}
