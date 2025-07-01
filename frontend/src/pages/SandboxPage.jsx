import React from 'react';
import SandboxControlPanel from '../components/sandbox/SandboxControlPanel';
import TopologyPage from './TopologyPage';
import ControlPanel from '../components/topology/ControlPanel'; // Import the details panel

const SandboxPage = () => {
  return (
    <div className="flex h-full w-full">
      {/* The sidebar now has two panels */}
      <div className="w-96 h-full flex-shrink-0 p-4 flex flex-col gap-4">
        {/* Panel 1: The main sandbox controls */}
        <div className="flex-shrink-0">
          <SandboxControlPanel />
        </div>
        {/* Panel 2: The details of the selected element */}
        <div className="flex-grow">
          <ControlPanel isSandbox={true} />
        </div>
      </div>
      <div className="flex-grow h-full">
        <TopologyPage isSandbox={true} />
      </div>
    </div>
  );
};

export default SandboxPage;