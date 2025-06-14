// Pfad: frontend/src/components/Map/PathPanel.jsx
import { Polyline } from "react-leaflet";

export default function PathPanel({ path }) {
  if (!Array.isArray(path)) return null;

  const positions = path.map(node => [node.lat, node.lon]);

  return (
    <Polyline
      positions={positions}
      color="blue"
      weight={5}
      opacity={0.8}
      dashArray="5, 10"
    />
  );
}
