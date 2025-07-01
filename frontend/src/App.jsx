import React, { useContext, useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from './layout/Layout';
import ProtectedRoute from './components/auth/ProtectedRoute';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import TopologyPage from './pages/TopologyPage';
import IncidentsPage from './pages/IncidentsPage';
import ForensicsPage from './pages/ForensicsPage';
import SandboxPage from './pages/SandboxPage';
import DeviceListPage from './pages/DeviceListPage';
import CommandMenu from './components/shared/CommandMenu';
import { CommandMenuContext } from './contexts/CommandMenuContext';
import { AuthContext } from './contexts/AuthContext';
import { TopologyProvider } from './contexts/TopologyContext';
import { SandboxProvider } from './contexts/SandboxContext';
// FIX: Ensure 3D page is imported and routed correctly
import Topology3DPage from './pages/Topology3DPage';

function App() {
  const { toggleCommandMenu } = useContext(CommandMenuContext);
  const { logout } = useContext(AuthContext);

  useEffect(() => {
    // ... (event listener logic if needed)
  }, [toggleCommandMenu, logout]);

  const AuthenticatedLayout = () => (
    <TopologyProvider>
      <SandboxProvider>
        <Layout />
      </SandboxProvider>
    </TopologyProvider>
  );

  return (
    <>
      <CommandMenu />
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/" element={<ProtectedRoute><AuthenticatedLayout /></ProtectedRoute>}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="topology" element={<TopologyPage />} />
          {/* 3D Topology is now its own, independent page */}
          <Route path="topology-3d" element={<Topology3DPage />} />
          <Route path="incidents" element={<IncidentsPage />} />
          <Route path="forensics" element={<ForensicsPage />} />
          <Route path="devices" element={<DeviceListPage />} />
          <Route path="sandbox" element={<SandboxPage />} />
        </Route>
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </>
  );
}

export default App;
