# Beispiel Leaflet-Integration (TopologyView.jsx)

import { Polyline, Tooltip } from "react-leaflet";
import useFiberLinks from "@/services/topology/useFiberLinks";

const { links, loading: linksLoading } = useFiberLinks();

{!linksLoading && links.map((link, idx) => (
  <Polyline
    key={idx}
    positions={link.path}
    color={link.status === "active" ? "green" : "red"}
    weight={4}
    eventHandlers={{
      click: () => {
        alert(
          "Verbindung: " + link.name +
          "\nTyp: " + link.type +
          "\nLänge: " + link.length_km + " km" +
          "\nDämpfung: " + link.attenuation_db + " dB"
        );
      }
    }}
  >
    <Tooltip sticky>{link.name}</Tooltip>
  </Polyline>
))}
