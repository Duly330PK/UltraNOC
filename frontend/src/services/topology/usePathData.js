// frontend/src/services/topology/usePathMetrics.js
import { useEffect, useState } from "react";

export default function usePathMetrics(deviceId) {
  const [pathMetrics, setPathMetrics] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!deviceId) {
      setPathMetrics([]);
      setLoading(false);
      return;
    }

    setLoading(true);
    fetch(`/api/path-metrics/${deviceId}`)
      .then((res) => res.json())
      .then((data) => {
        setPathMetrics(data.path || []);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Fehler beim Laden der Pfadmetriken:", err);
        setPathMetrics([]);
        setLoading(false);
      });
  }, [deviceId]);

  return { pathMetrics, loading };
}
