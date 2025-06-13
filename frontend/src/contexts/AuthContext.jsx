import React, { createContext, useState } from "react";
import axios from "axios";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("token") || null);

  const login = async (username, password) => {
    try {
      const res = await axios.post("http://localhost:8000/api/v1/auth/login", {
        username,
        password,
      });
      const accessToken = res.data.access_token;
      localStorage.setItem("token", accessToken);
      setToken(accessToken);
      return true;
    } catch (err) {
      console.error("Login fehlgeschlagen:", err);
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  const isAuthenticated = !!token;

  return (
    <AuthContext.Provider value={{ token, login, logout, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
}
