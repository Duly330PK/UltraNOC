// C:\noc_project\UltraNOC\frontend\src\contexts\AuthContext.jsx

import React, { createContext, useState } from "react";

import { NavLink } from "react-router-dom";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("token") || null);

  const login = async (username, password) => {
    try {
      const response = await fetch("http://localhost:8000/api/v1/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ username, password }),
      });

      const data = await response.json();

      if (response.ok && data.access_token) {
        localStorage.setItem("token", data.access_token);
        setToken(data.access_token);
        return true;
      } else {
        console.error("Login fehlgeschlagen:", data.detail || "Unbekannter Fehler");
        return false;
      }
    } catch (err) {
      console.error("Login Error:", err);
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    // Navigation erfolgt bewusst NICHT hier!
  };

  const isAuthenticated = !!token;

  return (
    <AuthContext.Provider value={{ token, login, logout, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
}
const Sidebar = () => {
  const navItems = [
    { path: "/dashboard", label: "Dashboard" },
    { path: "/devices", label: "Geräte" },
    { path: "/metrics", label: "Metriken" },
    { path: "/alerts", label: "Alarme" },
    { path: "/topology", label: "Topologie" },
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
                className={({ isActive }) => `block px-4 py-2 rounded transition ${isActive
                    ? "bg-nocblue text-white"
                    : "text-gray-300 hover:bg-gray-700"}`}
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
