import React, { useContext, useState, useEffect } from 'react';
import { TopologyContext } from '../../contexts/TopologyContext';
import DetailsTab from './tabs/DetailsTab';
import ActionsTab from './tabs/ActionsTab';
import TerminalTab from './tabs/TerminalTab';
import { Network, Server, Cpu, Cable, AlertCircle, Link as LinkIcon, X, GitMerge } from 'lucide-react';

const getIconForType = (type) => {
    if (!type) return <LinkIcon size={20} />;
    if (type.includes('Router')) return <Server size={20} />;
    if (type.includes('Gateway')) return <Cpu size={20} />;
    if (type.includes('OLT')) return <Cpu size={20} />;
    if (type.includes('Switch')) return <GitMerge size={20} />;
    if (type.includes('Muffe') || type.includes('Splitter')) return <Cable size={20} />;
    if (type.includes('ONT')) return <Network size={20} />;
    return <AlertCircle size={20} />;
};

const ControlPanel = () => {
    const { selectedElement, clearSelection } = useContext(TopologyContext);
    const [activeTab, setActiveTab] = useState('details');

    useEffect(() => {
        if (selectedElement) {
            const props = selectedElement.properties || {};
            const isLink = selectedElement.geometry?.type === 'LineString';
            const isPassive = props.is_passive || false;
            const isTerminalDisabled = isLink || isPassive;
            
            if (isTerminalDisabled && activeTab === 'terminal') {
                setActiveTab('details');
            }
        } else {
            setActiveTab('details');
        }
    }, [selectedElement, activeTab]);

    if (!selectedElement) {
        return (
            <div className="bg-noc-light-dark text-noc-text-secondary rounded-lg border border-noc-border p-6 h-full flex items-center justify-center text-center">
                <div>
                    <h3 className="font-bold text-noc-text">Kein Element ausgewählt</h3>
                    <p className="text-xs mt-1">Klicken Sie auf einen Knoten oder eine Verbindung auf der Karte, um Details anzuzeigen.</p>
                </div>
            </div>
        );
    }

    const props = selectedElement.properties;
    const isLink = selectedElement.geometry.type === 'LineString';
    const isPassive = props.is_passive || false;
    const title = isLink ? `Link: ${props.source} → ${props.target}` : props.label;
    const type = isLink ? props.type : props.type;

    const tabs = [
        { id: 'details', label: 'Details' },
        { id: 'actions', label: 'Aktionen', disabled: isLink },
        { id: 'terminal', label: 'Terminal', disabled: isLink || isPassive }
    ];

    return (
        <div className="bg-noc-light-dark rounded-lg border border-noc-border h-full flex flex-col">
            <div className="p-4 border-b border-noc-border flex items-center gap-4 relative">
                <div className="text-noc-blue flex-shrink-0">{getIconForType(type)}</div>
                <div className="flex-grow min-w-0">
                    <h2 className="text-lg font-bold text-noc-text truncate" title={title}>{title}</h2>
                    <p className="text-sm text-noc-text-secondary">{type}</p>
                </div>
                <button onClick={clearSelection} className="absolute top-2 right-2 text-noc-text-secondary hover:text-white p-1 rounded-full hover:bg-noc-border">
                    <X size={16} />
                </button>
            </div>

            <div className="border-b border-noc-border flex">
                {tabs.map(tab => !tab.disabled && (
                    <button 
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`flex-1 py-2 text-sm transition-colors duration-150 ${activeTab === tab.id ? 'bg-noc-blue text-white' : 'text-noc-text-secondary hover:bg-noc-border'}`}
                    >
                        {tab.label}
                    </button>
                ))}
            </div>

            <div className="p-4 flex-grow overflow-y-auto">
                {activeTab === 'details' && <DetailsTab element={selectedElement} />}
                {activeTab === 'actions' && <ActionsTab element={selectedElement} />}
                {activeTab === 'terminal' && <TerminalTab element={selectedElement} />}
            </div>
        </div>
    );
};

export default ControlPanel;