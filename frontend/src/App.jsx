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

function App() {
  const { toggleCommandMenu } = useContext(CommandMenuContext);
  const { logout } = useContext(AuthContext);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) e.preventDefault(), toggleCommandMenu();
    };
    const handleLogout = () => logout();
    document.addEventListener('keydown', handleKeyDown);
    window.addEventListener('logout-request', handleLogout);
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('logout-request', handleLogout);
    };
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
          {/* Route for 3D topology is removed to prevent errors until the component is ready */}
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