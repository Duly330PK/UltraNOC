
import L from "leaflet";

export function getDeviceIcon(type = "default") {
  const typeStyles = {
    core: { color: "#007bff", label: "C" },
    access: { color: "#17a2b8", label: "A" },
    olt: { color: "#28a745", label: "O" },
    ont: { color: "#ffc107", label: "T" },
    cpe: { color: "#6c757d", label: "E" },
    amp: { color: "#e83e8c", label: "AMP" },
    splitter: { color: "#6610f2", label: "S" },
    business: { color: "#fd7e14", label: "B" },
    default: { color: "#343a40", label: "?" }
  };

  const style = typeStyles[type] || typeStyles.default;

  return L.divIcon({
    html: `<div style="
      background:${style.color};
      color:#fff;
      width:24px;
      height:24px;
      border-radius:50%;
      display:flex;
      align-items:center;
      justify-content:center;
      font-size:12px;
    ">${style.label}</div>`,
    iconSize: [24, 24],
    className: "device-icon"
  });
}
