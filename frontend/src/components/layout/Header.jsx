import React from "react";
import LogoutButton from "./LogoutButton";

const Header = () => {
  return (
    <header className="bg-gray-800 text-white px-6 py-4 flex justify-between items-center shadow">
      <h1 className="text-2xl font-semibold">UltraNOC Dashboard</h1>
      <div className="flex items-center gap-2 text-sm">
        🔒 Eingeloggt
        <LogoutButton />
      </div>
    </header>
  );
};

export default Header;
