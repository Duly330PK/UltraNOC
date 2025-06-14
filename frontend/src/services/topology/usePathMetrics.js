// src/services/topology/usePathMetrics.js
import { useState, useEffect } from "react";
import axios from "axios";

export default function usePathMetrics(sourceId) {
  const [pathMetrics, setPathMetrics] = useState([]);

  useEffect(() => {
    if (!sourceId) return;

    axios
      .get(`/api/path/metrics/${sourceId}/cpe1`)
      .then((res) => {
        setPathMetrics(Array.isArray(res.data.path) ? res.data.path : []);
      })
      .catch(() => {
        setPathMetrics([]);
      });
  }, [sourceId]);

  return pathMetrics;
}
