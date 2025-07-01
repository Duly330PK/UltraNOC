import React from 'react';
import ForceGraph2DComponent from '../components/topology/ForceGraph2D';
import ControlPanel from '../components/topology/ControlPanel';

const Topology3DPage = () => {
  return (
    <div className="flex h-full w-full">
      <div className="flex-grow h-full">
        <ForceGraph2DComponent />
      </div>
      <div className="w-96 h-full flex-shrink-0">
        <ControlPanel />
      </div>
    </div>
  );
};

export default Topology3DPage;