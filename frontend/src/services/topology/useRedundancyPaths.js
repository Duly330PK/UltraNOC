// frontend/src/services/topology/useRedundancyPaths.js
import { useState, useEffect } from "react";
import axios from "axios";

export default function useRedundancyPaths(selectedDevice) {
  const [paths, setPaths] = useState({ primary: [], backup: [] });

  useEffect(() => {
    if (!selectedDevice) return;

    axios.get(`/api/topology/redundancy/${selectedDevice.id}`)
      .then(res => setPaths(res.data))
      .catch(err => console.error("Fehler beim Laden der Redundanzpfade:", err));
  }, [selectedDevice]);

  return paths;
}
