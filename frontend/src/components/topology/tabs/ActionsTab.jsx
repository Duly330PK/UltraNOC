import React, { useState, useEffect } from 'react';

const ActionButton = ({ label, onClick, color = 'noc-blue', disabled = false }) => (
  <button
    onClick={onClick}
    disabled={disabled}
    className={`w-full text-left px-4 py-2 mt-2 text-white rounded-md bg-${color} hover:bg-opacity-80 transition-all disabled:bg-noc-border disabled:text-noc-text-secondary disabled:cursor-not-allowed`}
  >
    {label}
  </button>
);

const ActionsTab = ({ element }) => {
    const [isChecking, setIsChecking] = useState(false);
    const [checkResult, setCheckResult] = useState(null);

    // Reset state when element changes
    useEffect(() => {
        setIsChecking(false);
        setCheckResult(null);
    }, [element.properties.id]);

    const handleApiAction = async (actionType, payload = {}) => {
        const token = localStorage.getItem('ultranoc_token');
        try {
            const response = await fetch(`/api/v1/simulation/devices/${element.properties.id}/action`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify({ type: actionType, payload }),
            });
            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Action failed');
            }
            return await response.json();
        } catch (error) {
            console.error(`Error performing action ${actionType}:`, error);
            setCheckResult({ error: error.message });
        }
    };

    const handleFieldServiceRequest = async () => {
        setIsChecking(true);
        setCheckResult(null);
        const result = await handleApiAction('request_field_service');
        setCheckResult(result);
        setIsChecking(false);
    };

    const renderActions = () => {
        const { type, status, is_passive } = element.properties;

        if (is_passive) {
            return (
                <div>
                    <ActionButton 
                        label={isChecking ? "Techniker ist unterwegs..." : "Außendienst anfordern"}
                        onClick={handleFieldServiceRequest} 
                        color="noc-purple"
                        disabled={isChecking}
                    />
                    {checkResult && (
                        <div className="mt-4 p-3 bg-noc-dark rounded-md border border-noc-border text-sm">
                            <h4 className="font-bold text-noc-text-secondary mb-2">Prüfbericht vom Außendienst:</h4>
                            {checkResult.error ? (
                                <p className="text-noc-red">{checkResult.error}</p>
                            ) : (
                                <>
                                    <p><strong>Status:</strong> <span className={checkResult.check_status === 'Nominal' ? 'text-noc-green' : 'text-noc-red'}>{checkResult.check_status}</span></p>
                                    <p><strong>Details:</strong> {checkResult.details}</p>
                                    <p><strong>Gemessener Verlust:</strong> {checkResult.measured_loss_db} dB</p>
                                    <p><strong>Empfehlung:</strong> {checkResult.recommendation}</p>
                                </>
                            )}
                        </div>
                    )}
                </div>
            );
        }

        switch (type) {
            case 'MPLS Core Router':
            case 'Broadband Network Gateway':
            case 'Aggregation Switch':
            case 'OLT':
            case 'ONT':
                return <>
                    <ActionButton label="Gerät neustarten" onClick={() => handleApiAction('reboot')} color="noc-yellow" disabled={status === 'rebooting'} />
                    <ActionButton label="Status auf 'offline' setzen" onClick={() => handleApiAction('set_status', { status: 'offline' })} color="noc-red" disabled={status === 'offline'} />
                    <ActionButton label="Status auf 'online' setzen" onClick={() => handleApiAction('set_status', { status: 'online' })} color="noc-green" disabled={status === 'online'}/>
                </>;
            default:
                return <p className="text-noc-text-secondary">Für dieses Element sind keine Aktionen verfügbar.</p>;
        }
    };

    return (
        <div>
            <h3 className="text-md font-bold text-noc-text mb-4">Verfügbare Aktionen</h3>
            {renderActions()}
        </div>
    );
};

export default ActionsTab;