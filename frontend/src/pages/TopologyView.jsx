import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import useTopologyData from "../services/topology/useTopologyData";
import AlarmPanel from "@/components/Widgets/AlarmPanel";
import MetricsPanel from "@/components/Widgets/MetricsPanel";
import L from "leaflet";
import markerIcon from "/leaflet/marker-icon.png";
import markerShadow from "/leaflet/marker-shadow.png";
import RedundancyPathPanel from "@/components/Map/RedundancyPathPanel";
import CableInfoPanel from "@/components/Map/CableInfoPanel";
import PathPanel from "@/components/Map/PathPanel";
import usePathData from "@/services/topology/usePathData";
import axios from "axios";
import usePathMetrics from "@/services/topology/usePathMetrics";
import PathMetricsPanel from "@/components/Map/PathMetricsPanel";

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

export default function TopologyView() {
  const { devices, loading } = useTopologyData();
  const [selectedDevice, setSelectedDevice] = useState(null);
  const [selectedLink, setSelectedLink] = useState(null);
  const [showCLI, setShowCLI] = useState(false);
  const [cliOutput, setCliOutput] = useState("");
  const [cliInput, setCliInput] = useState("");
  const [mockAlarms, setMockAlarms] = useState([]);
  const [primaryPath, setPrimaryPath] = useState([]);
  const [backupPath, setBackupPath] = useState([]);
  const path = usePathData(selectedDevice?.id);
  const rawMetrics = usePathMetrics(selectedDevice?.id);
  const pathMetrics = Array.isArray(rawMetrics) ? rawMetrics : [];

  const handleCLICommand = () => {
    const output = `> ${cliInput}\nErgebnis für '${cliInput}' auf ${selectedDevice?.name}`;
    setCliOutput((prev) => prev + "\n" + output);
    setCliInput("");
  };

  const mockMetrics = selectedDevice
    ? {
        tx: Math.floor(Math.random() * 1000),
        rx: Math.floor(Math.random() * 1000),
        delay: (Math.random() * 10).toFixed(2),
        loss: (Math.random() * 2).toFixed(2),
        status: Math.random() > 0.2 ? "online" : "offline",
      }
    : null;

  useEffect(() => {
    if (selectedDevice) {
      const randomAlarms = [
        { severity: "critical", msg: "Link Down on Port GE1/0/1" },
        { severity: "warning", msg: "High Temperature" },
        { severity: "info", msg: "Config change detected" },
      ];
      setMockAlarms(
        Math.random() > 0.5
          ? [randomAlarms[Math.floor(Math.random() * 3)]]
          : []
      );

      axios
        .get(`/api/topology/redundancy/${selectedDevice.id}`)
        .then((res) => {
          setPrimaryPath(res.data.primary || []);
          setBackupPath(res.data.backup || []);
        })
        .catch(() => {
          setPrimaryPath([]);
          setBackupPath([]);
        });
    }
  }, [selectedDevice]);

  return (
    <div className="w-full h-[80vh] rounded-2xl overflow-hidden shadow-xl relative">
      <MapContainer center={[51.2, 9.0]} zoom={7} className="w-full h-full z-0">
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />

        {!loading &&
          devices.map((device) => (
            <Marker
              key={device.id}
              position={[device.lat, device.lon]}
              eventHandlers={{
                click: () => {
                  setSelectedDevice(device);
                  setShowCLI(false);
                  setSelectedLink(null);
                },
              }}
            >
              <Popup>
                <div className="text-sm">
                  <strong>{device.name}</strong>
                  <br />
                  Typ: {device.type}
                  <br />
                  IP: {device.ip}
                </div>
              </Popup>
            </Marker>
          ))}

        <RedundancyPathPanel
          primaryPath={primaryPath}
          backupPath={backupPath}
          onLinkClick={(link) => {
            setSelectedLink(link);
            setSelectedDevice(null);
          }}
        />

        <PathPanel path={path} />
        <PathMetricsPanel pathMetrics={pathMetrics} />
      </MapContainer>

      <div className="absolute left-4 top-4 z-10">
        <AlarmPanel />
      </div>

      <div className="absolute bottom-4 right-4 z-10">
        <MetricsPanel />
      </div>

      {selectedLink && <CableInfoPanel link={selectedLink} />}

      {selectedDevice && (
        <div className="absolute right-4 top-4 bg-white text-black p-4 rounded-2xl shadow-2xl w-96 z-10">
          <h3 className="text-lg font-bold mb-2">Geräteinfo</h3>
          <p><strong>Name:</strong> {selectedDevice.name}</p>
          <p><strong>Typ:</strong> {selectedDevice.type}</p>
          <p><strong>IP:</strong> {selectedDevice.ip}</p>
          <p><strong>ID:</strong> {selectedDevice.id}</p>

          {mockMetrics && (
            <div className="mt-3 text-sm">
              <h4 className="font-semibold mb-1">Live-Metriken</h4>
              <ul className="list-disc ml-4">
                <li>TX: {mockMetrics.tx} bps</li>
                <li>RX: {mockMetrics.rx} bps</li>
                <li>Delay: {mockMetrics.delay} ms</li>
                <li>Loss: {mockMetrics.loss} %</li>
                <li>Status: <span className={mockMetrics.status === "online" ? "text-green-600 font-bold" : "text-red-500 font-bold"}>{mockMetrics.status}</span></li>
              </ul>
            </div>
          )}

          {mockAlarms.length > 0 && (
            <div className="mt-3 text-sm">
              <h4 className="font-semibold mb-1 text-red-600">Aktive Alarme</h4>
              <ul className="list-disc ml-4">
                {mockAlarms.map((alarm, idx) => (
                  <li key={idx} className={
                    alarm.severity === "critical" ? "text-red-600" :
                    alarm.severity === "warning" ? "text-yellow-600" :
                    "text-gray-600"
                  }>
                    [{alarm.severity.toUpperCase()}] {alarm.msg}
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div className="mt-4 flex justify-between">
            <button
              onClick={() => setSelectedDevice(null)}
              className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600"
            >
              Schließen
            </button>
            <button
              onClick={() => setShowCLI((prev) => !prev)}
              className="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              {showCLI ? "CLI schließen" : "CLI öffnen"}
            </button>
          </div>

          {showCLI && (
            <div className="mt-4 bg-black text-green-400 font-mono text-sm p-2 rounded h-40 overflow-y-auto">
              <pre>{cliOutput || "CLI gestartet. Geben Sie einen Befehl ein."}</pre>
            </div>
          )}

          {showCLI && (
            <div className="mt-2 flex">
              <input
                type="text"
                className="flex-1 px-2 py-1 border rounded-l bg-gray-100"
                placeholder="Befehl eingeben..."
                value={cliInput}
                onChange={(e) => setCliInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleCLICommand()}
              />
              <button
                onClick={handleCLICommand}
                className="px-3 bg-green-600 text-white rounded-r hover:bg-green-700"
              >
                Ausführen
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
