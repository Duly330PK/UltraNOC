
// frontend/src/assets/icons/generateDeviceIcon.js
import L from "leaflet";

export function getDeviceIcon(type) {
  const colorMap = {
    core: "blue",
    access: "green",
    customer: "orange",
    passive: "gray"
  };

  const color = colorMap[type] || "black";
  return L.divIcon({
    className: "",
    html: `<div style="background:${color};width:12px;height:12px;border-radius:50%"></div>`,
    iconSize: [12, 12]
  });
}
