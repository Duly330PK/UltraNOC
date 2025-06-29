import React from 'react';

const IncidentGraph = ({ incident }) => {
  // Dies ist eine statische Darstellung des Graphen aus dem Bild.
  // Eine dynamische Version würde eine Graphen-Bibliothek (D3, VisX)
  // und eine Layout-Engine benötigen, um die Knoten und Kanten basierend
  // auf den `incident.events`-Daten zu positionieren.
  const nodes = {
      '04': { x: '15%', y: '25%', label: 'Host-base firewall blocked' },
      '06': { x: '20%', y: '70%', label: 'Failed SSH login' },
      '03': { x: '40%', y: '15%', label: 'Successful SSH login' },
      '38': { x: '45%', y: '45%', label: 'Failed SSH login' },
      '14': { x: '50%', y: '75%', label: 'Failed network login' },
      '29': { x: '60%', y: '90%', label: 'Failed network login' },
      '09': { x: '65%', y: '10%', label: 'Failed SSH login' },
      '22': { x: '70%', y: '55%', label: 'Host-base firewall blocked' },
      '13': { x: '80%', y: '25%', label: 'Account logged out' },
      '07': { x: '90%', y: '10%', label: 'Failed network login' },
  };

  const links = [
      ['04', '06'], ['04', '03'], ['06', '14'], ['03', '09'], ['03', '38'],
      ['38', '14'], ['38', '22'], ['14', '29'], ['09', '07'], ['09', '13'],
      ['22', '13'], ['22', '09']
  ];

  return (
    <div className="w-full h-full bg-noc-light-dark rounded-lg border border-noc-border p-6 relative overflow-hidden">
      <h2 className="text-xl font-bold text-noc-text">{incident.title}</h2>
      <span className="text-sm bg-noc-red text-white px-2 py-1 rounded-full absolute top-6 right-6">Malicious</span>

      <div className="mt-10 relative h-full">
        <svg className="absolute inset-0 w-full h-full">
            <defs>
                <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 0 L 10 5 L 0 10 z" fill="#30363d" />
                </marker>
            </defs>
            {links.map(([source, target], i) => (
                <line key={i} x1={nodes[source].x} y1={nodes[source].y} x2={nodes[target].x} y2={nodes[target].y} stroke="#30363d" markerEnd="url(#arrow)" />
            ))}
        </svg>

        {Object.entries(nodes).map(([id, {x, y, label}]) => (
            <div key={id} className="absolute" style={{ left: x, top: y, transform: 'translate(-50%, -50%)' }}>
                <div className="w-12 h-12 rounded-full border-2 border-noc-blue/50 bg-noc-dark flex items-center justify-center font-bold text-noc-blue text-lg">
                    <div className="w-10 h-10 rounded-full border-2 border-noc-blue/80 bg-noc-dark/50 flex items-center justify-center">{id}</div>
                </div>
                <div className="text-center text-xs mt-2 w-24 text-noc-text-secondary">{label}</div>
            </div>
        ))}
      </div>
    </div>
  );
};
export default IncidentGraph;