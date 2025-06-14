// C:\noc_project\UltraNOC\frontend\src\components\Widgets\ClockWidget.jsx

import React, { useEffect, useState } from "react";

export default function ClockWidget() {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-nocgray p-6 rounded-2xl shadow-lg">
      <h2 className="text-xl font-semibold mb-2">🕒 Aktuelle Uhrzeit</h2>
      <p className="text-2xl font-mono">
        {time.toLocaleTimeString("de-DE")}
      </p>
    </div>
  );
}
