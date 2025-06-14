// C:\noc_project\UltraNOC\frontend\src\pages\DeviceOverviewPage.jsx

import React from "react";
import DeviceCard from "../components/devices/DeviceCard";

const mockDevices = [
  {
    name: "Cisco ASR1002-X",
    type: "Core Router",
    status: "online",
    location: "Köln / RZ1",
  },
  {
    name: "Huawei MA5800-X17",
    type: "OLT",
    status: "online",
    location: "Düsseldorf / Aggregation",
  },
  {
    name: "FortiGate 100F",
    type: "Firewall",
    status: "offline",
    location: "Frankfurt / Edge",
  },
];

const DeviceOverviewPage = () => {
  return (
    <div className="p-6 bg-gray-900 min-h-screen text-white">
      <h1 className="text-2xl font-bold mb-6">Geräteübersicht</h1>
      <div className="flex flex-wrap gap-6">
        {mockDevices.map((device, index) => (
          <DeviceCard key={index} {...device} />
        ))}
      </div>
    </div>
  );
};

export default DeviceOverviewPage;
