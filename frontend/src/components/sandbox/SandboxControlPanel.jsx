// frontend/src/components/sandbox/SandboxControlPanel.jsx

import React, { useContext } from 'react';
import { SandboxContext } from '../../contexts/SandboxContext';
import { Plus, GitPullRequest, Save, FolderOpen, Settings } from 'lucide-react';

const deviceTemplates = [
    { type: 'Core Router', label: 'Core Router' },
    { type: 'OLT', label: 'OLT' },
    { type: 'Muffe', label: 'Muffe' },
    { type: 'ONT', label: 'ONT' },
];

const SandboxControlPanel = () => {
    const { sandboxMode, setSandboxMode, nodeTypeToAdd, setNodeTypeToAdd, setLinkSourceNode } = useContext(SandboxContext);

    const handleAddNode = () => {
        setSandboxMode('addNode');
        alert('Klicken Sie auf die Karte, um einen neuen Knoten zu platzieren.');
    };

    const handleAddLink = () => {
        setSandboxMode('addLinkStart');
        setLinkSourceNode(null); // Link-Prozess zurücksetzen
        alert('Wählen Sie einen Start-Knoten auf der Karte aus.');
    };

    return (
        <div className="bg-noc-light-dark text-noc-text rounded-lg border border-noc-border p-4 h-full flex flex-col space-y-4">
            <h3 className="text-xl font-bold mb-4">Sandbox Steuerung</h3>
            
            <div className="grid grid-cols-2 gap-2">
                <button 
                    onClick={handleAddNode} 
                    className={`flex items-center justify-center gap-2 py-2 px-3 rounded-md text-sm font-medium transition-colors ${sandboxMode === 'addNode' ? 'bg-noc-blue text-white' : 'bg-noc-border hover:bg-noc-blue'}`}
                >
                    <Plus size={16}/> Knoten
                </button>
                <button 
                    onClick={handleAddLink} 
                    className={`flex items-center justify-center gap-2 py-2 px-3 rounded-md text-sm font-medium transition-colors ${sandboxMode.includes('addLink') ? 'bg-noc-blue text-white' : 'bg-noc-border hover:bg-noc-blue'}`}
                >
                    <GitPullRequest size={16}/> Verbindung
                </button>
            </div>

            {sandboxMode === 'addNode' && (
                <div className="mt-2">
                    <label className="block text-sm text-noc-text-secondary mb-1">Gerätetyp:</label>
                    <select 
                        value={nodeTypeToAdd} 
                        onChange={(e) => setNodeTypeToAdd(e.target.value)}
                        className="w-full p-2 bg-noc-dark border border-noc-border rounded-md text-noc-text"
                    >
                        {deviceTemplates.map(template => (
                            <option key={template.type} value={template.type}>{template.label}</option>
                        ))}
                    </select>
                </div>
            )}
            
            <div className="border-t border-noc-border pt-4 mt-auto space-y-2">
                <button className="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-md text-sm font-medium bg-noc-green hover:bg-opacity-80 text-white">
                    <Save size={16}/> Topologie Speichern
                </button>
                <button className="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-md text-sm font-medium bg-noc-purple hover:bg-opacity-80 text-white">
                    <Settings size={16}/> Szenario Editor
                </button>
            </div>
        </div>
    );
};

export default SandboxControlPanel;
