import React from 'react';

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
    const handleAction = async (actionType, payload = {}) => {
        const token = localStorage.getItem('ultranoc_token');
        try {
            await fetch(`/api/v1/simulation/devices/${element.properties.id}/action`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify({ type: actionType, payload }),
            });
        } catch (error) {
            console.error(`Fehler bei Aktion ${actionType}:`, error);
        }
    };

    const renderActions = () => {
        const { type, status } = element.properties;
        switch (type) {
            case 'Core Router':
            case 'OLT':
            case 'ONT':
                return <>
                    <ActionButton label="Gerät neustarten" onClick={() => handleAction('reboot')} color="noc-yellow" disabled={status === 'rebooting'} />
                    <ActionButton label="Status auf 'offline' setzen" onClick={() => handleAction('set_status', { status: 'offline' })} color="noc-red" disabled={status === 'offline'} />
                    <ActionButton label="Status auf 'online' setzen" onClick={() => handleAction('set_status', { status: 'online' })} color="noc-green" disabled={status === 'online'}/>
                </>;
            case 'Muffe':
                return <ActionButton label="Außendiensteinsatz anfordern" onClick={() => handleAction('request_field_service')} disabled={status === 'maintenance'} />;
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