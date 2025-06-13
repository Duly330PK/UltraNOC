import React from "react";

const DWDMPathGraph = ({ path }) => {
  if (!path || path.length === 0) {
    return <div className="text-gray-400">Kein Signalpfad verfügbar.</div>;
  }

  return (
    <div className="bg-nocgray p-4 rounded-2xl shadow-md">
      <h2 className="text-xl font-semibold mb-4 text-nocblue">DWDM Signalpfad</h2>
      <div className="flex items-center overflow-x-auto space-x-4">
        {path.map((node, index) => (
          <React.Fragment key={index}>
            <div className="flex flex-col items-center">
              <div className="w-10 h-10 rounded-full bg-nocblue flex items-center justify-center text-white font-bold">
                {node}
              </div>
              <span className="text-sm mt-1">{node}</span>
            </div>
            {index < path.length - 1 && (
              <div className="w-12 h-1 bg-white rounded-full" />
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};

export default DWDMPathGraph;
