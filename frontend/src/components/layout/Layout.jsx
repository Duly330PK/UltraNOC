// C:\noc_project\UltraNOC\frontend\src\components\layout\Layout.jsx

import React from "react";
import Sidebar from "./Sidebar";
import Header from "./Header";
import { Outlet } from "react-router-dom";

const Layout = () => {
  return (
    <div className="flex h-screen bg-gray-900 text-white">
      <Sidebar />
      <div className="flex flex-col flex-grow overflow-hidden">
        <Header />
        <main className="flex-grow overflow-y-auto p-6 bg-gray-800">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;
