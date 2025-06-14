// Pfad: frontend/src/components/Map/RedundancyPathPanel.jsx
import React from "react";
import { Polyline, Tooltip } from "react-leaflet";

export default function RedundancyPathPanel({ primaryPath, backupPath }) {
  return (
    <>
      {primaryPath?.length > 1 && (
        <Polyline
          positions={primaryPath.map((node) => [node.lat, node.lon])}
          pathOptions={{ color: "green", dashArray: "0" }}
        >
          <Tooltip sticky>Primärpfad</Tooltip>
        </Polyline>
      )}

      {backupPath?.length > 1 && (
        <Polyline
          positions={backupPath.map((node) => [node.lat, node.lon])}
          pathOptions={{ color: "red", dashArray: "8,4" }}
        >
          <Tooltip sticky>Redundanzpfad</Tooltip>
        </Polyline>
      )}
    </>
  );
}
