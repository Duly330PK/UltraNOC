// C:\noc_project\UltraNOC\frontend\src\routes\AppRouter.jsx

import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "../pages/LoginPage";
import DashboardPage from "../pages/DashboardPage";
import DeviceOverviewPage from "../pages/DeviceOverviewPage";
import ProtectedRoute from "../components/ProtectedRoute";
import Layout from "../components/Layout/Layout";

export default function AppRouter() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="devices" element={<DeviceOverviewPage />} />
        </Route>
        <Route path="*" element={<LoginPage />} />
      </Routes>
    </Router>
  );
}
