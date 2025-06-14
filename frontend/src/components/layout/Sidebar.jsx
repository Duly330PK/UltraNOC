// C:\noc_project\UltraNOC\frontend\src\components\layout\Sidebar.jsx

import React from "react";
import { NavLink } from "react-router-dom";

const Sidebar = () => {
  const navItems = [
    { path: "/dashboard", label: "Dashboard" },
    { path: "/devices", label: "Geräte" },
    { path: "/metrics", label: "Metriken" },
    { path: "/alerts", label: "Alarme" },
    { path: "/export", label: "Export" },
  ];

  return (
    <aside className="w-64 h-screen bg-nocgray text-white flex flex-col">
      <div className="text-center text-2xl font-bold py-6 border-b border-gray-800">
        UltraNOC
      </div>
      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          {navItems.map((item) => (
            <li key={item.path}>
              <NavLink
                to={item.path}
                className={({ isActive }) =>
                  `block px-4 py-2 rounded transition ${
                    isActive
                      ? "bg-nocblue text-white"
                      : "text-gray-300 hover:bg-gray-700"
                  }`
                }
              >
                {item.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
};

export default Sidebar;
