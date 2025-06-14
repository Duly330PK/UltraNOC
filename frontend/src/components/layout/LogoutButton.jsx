// C:\noc_project\UltraNOC\frontend\src\components\Layout\LogoutButton.jsx

import React, { useContext } from "react";
import { AuthContext } from "../../contexts/AuthContext"; // ✅ korrigierter Pfad

const LogoutButton = () => {
  const { logout } = useContext(AuthContext);

  return (
    <button
      onClick={logout}
      className="ml-4 px-3 py-1 bg-red-600 rounded hover:bg-red-700 text-sm"
    >
      Logout
    </button>
  );
};

export default LogoutButton;
