// frontend/src/components/dashboard/ScenarioControl.jsx

import React, { useState } from 'react';
import { PlayCircle, Zap } from 'lucide-react';

// Die Namen der Szenarien, die im Backend unter 'backend/app/data/scenarios/' liegen
const scenarios = [
    { id: 'ddos_attack', name: 'DDoS-Angriff', description: 'Simuliert einen DDoS-Angriff auf den Core-Router.', icon: <Zap size={16} className="text-noc-red" /> },
    { id: 'insider_threat', name: 'Insider-Bedrohung', description: 'Ein Techniker schaltet versehentlich einen Uplink ab.', icon: <PlayCircle size={16} className="text-noc-yellow" /> }
];

const ScenarioControl = () => {
    const [loadingScenario, setLoadingScenario] = useState(null);

    const triggerScenario = async (scenarioId) => {
        setLoadingScenario(scenarioId);
        const token = localStorage.getItem('ultranoc_token');
        try {
            const response = await fetch(`/api/v1/scenarios/load/${scenarioId}`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const result = await response.json();
                alert(`Szenario gestartet: ${result.message}`);
            } else {
                const error = await response.json();
                alert(`Fehler beim Starten des Szenarios: ${error.detail || 'Unbekannter Fehler'}`);
            }
        } catch (error) {
            alert(`Ein Netzwerkfehler ist aufgetreten: ${error.message}`);
        } finally {
            setLoadingScenario(null);
        }
    };

    return (
        <div className="bg-noc-light-dark p-4 rounded-lg border border-noc-border col-span-1 lg:col-span-2">
            <h2 className="text-xl font-bold text-noc-text mb-4 px-2">Szenarien starten</h2>
            <div className="space-y-3">
                {scenarios.map(scenario => (
                    <div key={scenario.id} className="bg-noc-dark p-3 rounded-md flex items-center gap-4">
                        <div className="flex-shrink-0">{scenario.icon}</div>
                        <div className="flex-grow">
                            <h3 className="font-bold text-noc-text">{scenario.name}</h3>
                            <p className="text-xs text-noc-text-secondary">{scenario.description}</p>
                        </div>
                        <button
                            onClick={() => triggerScenario(scenario.id)}
                            disabled={!!loadingScenario}
                            className="bg-noc-blue text-white px-4 py-1 rounded-md text-sm font-semibold hover:bg-opacity-80 disabled:bg-noc-border disabled:cursor-not-allowed"
                        >
                            {loadingScenario === scenario.id ? 'Lädt...' : 'Start'}
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ScenarioControl;