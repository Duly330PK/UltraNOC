
import { useEffect, useState } from "react";
import axios from "axios";

export default function useFiberLinks() {
  const [links, setLinks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get("/api/topology/links")
      .then((res) => setLinks(res.data || []))
      .catch((err) => console.error("Fehler beim Laden der Links:", err))
      .finally(() => setLoading(false));
  }, []);

  return { links, loading };
}
