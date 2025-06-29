// frontend/src/pages/SandboxPage.jsx

import React from 'react';
import SandboxControlPanel from '../components/sandbox/SandboxControlPanel';
import TopologyPage from './TopologyPage'; // Wir verwenden die Haupt-Topologie-Seite wieder

const SandboxPage = () => {
  return (
    <div className="flex h-full w-full">
      <div className="w-96 h-full flex-shrink-0 p-4">
        <SandboxControlPanel />
      </div>
      <div className="flex-grow h-full">
        <TopologyPage isSandbox={true} />
      </div>
    </div>
  );
};

export default SandboxPage;