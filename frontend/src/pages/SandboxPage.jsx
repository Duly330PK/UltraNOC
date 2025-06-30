import React from 'react';
// KORRIGIERT: Wir importieren die existierende 3D-Topologie-Seite, die den Sandbox-Modus unterstützt.
import Topology3DPage from './Topology3DPage'; 
import SandboxControlPanel from '../components/sandbox/SandboxControlPanel';

const SandboxPage = () => {
  return (
    <div className="flex h-full w-full">
      <div className="w-96 h-full flex-shrink-0 p-4">
        {/* Das Control Panel bleibt dasselbe */}
        <SandboxControlPanel />
      </div>
      <div className="flex-grow h-full">
        {/* KORRIGIERT: Wir rendern die korrekte Komponente und übergeben ihr den Sandbox-Prop */}
        <Topology3DPage isSandbox={true} />
      </div>
    </div>
  );
};

export default SandboxPage;