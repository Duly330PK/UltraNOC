// frontend/src/components/dashboard/SecurityControl.jsx

import React, { useState } from 'react';
import { Power, PowerOff, RefreshCw } from 'lucide-react';

const SecurityControl = () => {
    const [isEnabled, setIsEnabled] = useState(true);
    const [isLoading, setIsLoading] = useState(false);

    const callApi = async (endpoint, payload) => {
        setIsLoading(true);
        const token = localStorage.getItem('ultranoc_token');
        try {
            const response = await fetch(`/api/v1/simulation/${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(payload)
            });
            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || "Ein Fehler ist aufgetreten.");
            }
            return await response.json();
        } catch (error) {
            alert(`Fehler: ${error.message}`);
        } finally {
            setIsLoading(false);
        }
    };

    const handleToggle = async () => {
        const newState = !isEnabled;
        const result = await callApi('security/toggle', { enabled: newState });
        if (result) {
            setIsEnabled(newState);
            alert(result.message);
        }
    };

    const handleReset = async () => {
        if (window.confirm("Sind Sie sicher, dass Sie alle Sicherheits-Events und Incidents zurücksetzen möchten?")) {
            await callApi('security/reset', {});
        }
    };

    return (
        <div className="bg-noc-light-dark p-4 rounded-lg border border-noc-border">
            <h2 className="text-xl font-bold text-noc-text mb-4 px-2">Sicherheits-Simulation</h2>
            <div className="space-y-4">
                <div className="flex items-center justify-between bg-noc-dark p-3 rounded-md">
                    <div>
                        <h3 className="font-bold text-noc-text">Event-Generierung</h3>
                        <p className={`text-sm font-bold ${isEnabled ? 'text-noc-green' : 'text-noc-red'}`}>
                            {isEnabled ? 'Aktiv' : 'Inaktiv'}
                        </p>
                    </div>
                    <button
                        onClick={handleToggle}
                        disabled={isLoading}
                        className={`p-2 rounded-full transition-colors disabled:opacity-50 ${isEnabled ? 'bg-noc-green/20 hover:bg-noc-green/40' : 'bg-noc-red/20 hover:bg-noc-red/40'}`}
                    >
                        {isEnabled ? <PowerOff className="text-noc-red" /> : <Power className="text-noc-green" />}
                    </button>
                </div>
                 <div className="flex items-center justify-between bg-noc-dark p-3 rounded-md">
                    <div>
                        <h3 className="font-bold text-noc-text">Events & Incidents</h3>
                        <p className="text-sm text-noc-text-secondary">Setzt alle Zähler zurück.</p>
                    </div>
                    <button
                        onClick={handleReset}
                        disabled={isLoading}
                        className="bg-noc-border p-2 rounded-full hover:bg-noc-blue/40 transition-colors disabled:opacity-50"
                    >
                        <RefreshCw className="text-noc-blue" />
                    </button>
                </div>
            </div>
        </div>
    );
};

export default SecurityControl;