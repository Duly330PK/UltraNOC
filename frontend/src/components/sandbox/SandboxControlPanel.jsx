import React, { useContext, useState } from 'react';
import { Plus, GitPullRequest, Save } from 'lucide-react';
import { TopologyContext } from '../../contexts/TopologyContext';
import { SandboxContext } from '../../contexts/SandboxContext';

const SandboxControlPanel = () => {
    const { topology } = useContext(TopologyContext);
    const { sandboxMode, setSandboxMode, nodeTypeToAdd, setNodeTypeToAdd, setLinkSourceNode, deviceTemplates } = useContext(SandboxContext);
    const [isSaving, setIsSaving] = useState(false);

    const handleSaveTopology = async () => {
        setIsSaving(true);
        const token = localStorage.getItem('ultranoc_token');
        try {
            const response = await fetch('/api/v1/sandbox/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify(topology)
            });
            if (response.ok) {
                alert('Topologie erfolgreich gespeichert!');
            } else {
                const error = await response.json();
                alert(`Fehler beim Speichern: ${error.detail}`);
            }
        } catch (error) {
            console.error("Save failed:", error);
            alert('Netzwerkfehler beim Speichern der Topologie.');
        } finally {
            setIsSaving(false);
        }
    };
    
    const handleStartAddLink = () => {
        setSandboxMode('addLinkStart');
        setLinkSourceNode(null);
    };

    return (
        <div className="bg-noc-light-dark text-noc-text rounded-lg border border-noc-border p-4 h-full flex flex-col space-y-4">
            <h3 className="text-xl font-bold mb-4">Sandbox Steuerung</h3>
            
            <div className="grid grid-cols-2 gap-2">
                <button 
                    onClick={() => setSandboxMode('addNode')} 
                    className={`flex items-center justify-center gap-2 py-2 px-3 rounded-md text-sm font-medium transition-colors ${sandboxMode === 'addNode' ? 'bg-noc-blue text-white' : 'bg-noc-border hover:bg-noc-blue'}`}
                >
                    <Plus size={16}/> Knoten
                </button>
                <button 
                    onClick={handleStartAddLink} 
                    className={`flex items-center justify-center gap-2 py-2 px-3 rounded-md text-sm font-medium transition-colors ${sandboxMode.startsWith('addLink') ? 'bg-noc-blue text-white' : 'bg-noc-border hover:bg-noc-blue'}`}
                >
                    <GitPullRequest size={16}/> Verbindung
                </button>
            </div>
            
            {sandboxMode.startsWith('addLink') && (
                <div className="p-2 text-center bg-noc-blue/20 text-noc-blue rounded-md text-sm">
                    {sandboxMode === 'addLinkStart' ? 'Startknoten auf der Karte wählen.' : 'Zielknoten auf der Karte wählen.'}
                </div>
            )}

            <div>
                <label className="block text-sm text-noc-text-secondary mb-1">Gerätetyp für neue Knoten:</label>
                <select 
                    value={nodeTypeToAdd} 
                    onChange={(e) => setNodeTypeToAdd(e.target.value)}
                    className="w-full p-2 bg-noc-dark border border-noc-border rounded-md text-noc-text"
                >
                    {deviceTemplates.map(template => (
                        <option key={template.id} value={template.id}>{template.name}</option>
                    ))}
                </select>
            </div>
            
            <div className="border-t border-noc-border pt-4 mt-auto space-y-2">
                <button 
                    onClick={handleSaveTopology}
                    disabled={isSaving}
                    className="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-md text-sm font-medium bg-noc-green text-white hover:bg-opacity-80 disabled:opacity-50"
                >
                    <Save size={16}/> {isSaving ? 'Speichert...' : 'Topologie Speichern'}
                </button>
            </div>
        </div>
    );
};

export default SandboxControlPanel;