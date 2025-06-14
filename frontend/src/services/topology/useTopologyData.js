// frontend/src/services/topology/useTopologyData.js
import { useEffect, useState } from "react";
import axios from "axios";

export default function useTopologyData() {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get("/api/v1/topology/core")
      .then((res) => {
        setDevices(res.data.devices || []);
      })
      .catch((err) => {
        console.error("Fehler beim Laden der Topologie:", err);
      })
      .finally(() => setLoading(false));
  }, []);

  return { devices, loading };
}
