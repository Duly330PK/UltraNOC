// frontend/src/components/Map/CableInfoPanel.jsx
import { Polyline, Tooltip } from "react-leaflet";
import { useState } from "react";

function haversineDistance([lat1, lon1], [lat2, lon2]) {
  const toRad = (deg) => (deg * Math.PI) / 180;
  const R = 6371;
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

export default function CableInfoPanel({ devices }) {
  const [selectedCable, setSelectedCable] = useState(null);

  const links = [];
  for (let i = 0; i < devices.length - 1; i++) {
    const from = devices[i];
    const to = devices[i + 1];
    const positions = [
      [from.lat, from.lon],
      [to.lat, to.lon],
    ];
    const lengthKm = haversineDistance(positions);
    const attenuation = 0.22 * lengthKm;

    links.push({
      id: `${from.id}-${to.id}`,
      from,
      to,
      positions,
      lengthKm: lengthKm.toFixed(2),
      attenuation: attenuation.toFixed(2),
    });
  }

  return (
    <>
      {links.map((link) => (
        <Polyline
          key={link.id}
          positions={link.positions}
          color={selectedCable === link.id ? "red" : "blue"}
          weight={4}
          dashArray="4"
          eventHandlers={{
            click: () => setSelectedCable(link.id),
          }}
        >
          <Tooltip sticky>
            {selectedCable === link.id ? (
              <div>
                <strong>Verbindung:</strong> {link.from.name} → {link.to.name}
                <br />
                <strong>Länge:</strong> {link.lengthKm} km
                <br />
                <strong>Dämpfung:</strong> {link.attenuation} dB
                <br />
                <strong>Kabeltyp:</strong> G.652.D
              </div>
            ) : (
              `${link.from.name} → ${link.to.name}`
            )}
          </Tooltip>
        </Polyline>
      ))}
    </>
  );
}
