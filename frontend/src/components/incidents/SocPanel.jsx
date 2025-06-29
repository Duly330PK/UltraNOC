import React, { useState } from 'react';
import { ShieldCheck, UserCheck, AlertOctagon, Files, ShieldOff, MessageSquare } from 'lucide-react';

const StatItem = ({ icon, label, value }) => (
    <div>
        <div className="text-xs text-noc-text-secondary flex items-center gap-2">{icon}{label}</div>
        <div className="text-lg font-bold text-noc-text">{value}</div>
    </div>
);

const SocPanel = ({ incident }) => {
  const [llmAnalysis, setLlmAnalysis] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  // In einer echten App würde der Verlauf hier aus einem Context oder State kommen
  // const [llmHistory, setLlmHistory] = useState([]); 

  const handleLlmRequest = async (type) => {
    setIsAnalyzing(true);
    setLlmAnalysis('Analysiere...');

    // Hier würde der API-Aufruf an das Backend erfolgen,
    // das dann mit dem LLM kommuniziert.
    // const response = await fetch('/api/v1/llm/analyze', { ... });

    // Simulierte Antwort für die Demo
    const simulatedResponse = type === 'root_cause' 
      ? "Root Cause: Wahrscheinlich ein erfolgreicher Brute-Force-Angriff, der zu einem Credential-Diebstahl führte, gefolgt von lateralen Bewegungen."
      : "Mitigations: 1. Betroffenen Host sofort aus dem Netzwerk isolieren. 2. Alle Passwörter des kompromittierten Users zurücksetzen. 3. SSH-Logs auf weitere verdächtige Aktivitäten prüfen.";

    setTimeout(() => {
        setLlmAnalysis(simulatedResponse);
        // setLlmHistory(prev => [...prev, {role: 'user', content: prompt}, {role: 'assistant', content: simulatedResponse}]);
        setIsAnalyzing(false);
    }, 1500);
  };

  return (
    <div className="bg-noc-light-dark rounded-lg border border-noc-border h-full flex flex-col p-6 text-noc-text">
        <div>
            <h3 className="text-lg font-bold">Overview</h3>
            <p className="text-sm text-noc-text-secondary mt-2">{incident.summary}</p>
        </div>

        <div className="grid grid-cols-2 gap-y-4 gap-x-2 mt-6">
            <StatItem icon={<AlertOctagon size={14}/>} label="Events" value={incident.metrics.events} />
            <StatItem icon={<UserCheck size={14}/>} label="Assignee" value={incident.assignee} />
            <StatItem icon={<ShieldOff size={14}/>} label="Attackers" value={incident.metrics.attackers} />
            <StatItem icon={<Files size={14}/>} label="Artifacts" value={incident.metrics.artifacts} />
        </div>

        <div className="mt-6 border-t border-noc-border pt-4">
            <h4 className="text-md font-bold text-noc-text-secondary">SOC-Analyst (LLM-Powered)</h4>
            <div className="flex gap-2 mt-2">
                <button onClick={() => handleLlmRequest('root_cause')} disabled={isAnalyzing} className="text-xs bg-noc-border py-1 px-2 rounded hover:bg-noc-blue disabled:opacity-50">Suggest Root Cause</button>
                <button onClick={() => handleLlmRequest('mitigation')} disabled={isAnalyzing} className="text-xs bg-noc-border py-1 px-2 rounded hover:bg-noc-green disabled:opacity-50">Recommend Mitigations</button>
            </div>
            {llmAnalysis && (
                <div className="mt-2 p-3 bg-noc-dark rounded text-xs text-noc-text-secondary border border-noc-border">
                    {llmAnalysis}
                </div>
            )}
        </div>

        <div className="mt-auto pt-6 flex gap-4">
            <button className="flex-1 bg-noc-border text-noc-text-secondary py-2 rounded-md hover:opacity-80">Found a mistake</button>
            <button className="flex-1 bg-noc-blue text-white py-2 rounded-md hover:opacity-80">Change status</button>
        </div>
    </div>
  );
};
export default SocPanel;