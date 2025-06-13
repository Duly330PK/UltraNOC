import React, { useEffect, useState } from "react";

function ClockWidget() {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-4 rounded-xl shadow bg-white text-center">
      <h2 className="text-xl font-semibold">Systemzeit</h2>
      <p className="text-2xl mt-2 font-mono">{time.toLocaleTimeString()}</p>
    </div>
  );
}

export default ClockWidget;
