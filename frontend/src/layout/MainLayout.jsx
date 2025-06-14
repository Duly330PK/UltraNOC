// C:\noc_project\UltraNOC\frontend\src\Layout\MainLayout.jsx

import React from "react";
import { Outlet } from "react-router-dom";
import Sidebar from "../contexts/AuthContext";
import Header from "../components/Layout/Header";

function MainLayout() {
  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar />
      <div className="flex flex-col flex-1">
        <Header />
        <main className="flex-1 p-4 overflow-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default MainLayout;
