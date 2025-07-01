import React, { useContext } from 'react';
import { Plus, GitPullRequest, Save, FolderOpen } from 'lucide-react';
import { SandboxContext } from '../../contexts/SandboxContext';

const SandboxControlPanel = () => {
    const { 
        mode = 'view',
        setMode = () => {},
        templates = [], 
        isLoading, // NEU: isLoading-Status aus dem Context holen
        selectedTemplateId = '', 
        setSelectedTemplateId = () => {}, 
        setLinkSourceNode = () => {}
    } = useContext(SandboxContext) || {};
    
    const handleStartAddLink = () => {
        setMode('addLinkStart');
        setLinkSourceNode(null);
        alert('Modus "Verbindung hinzufügen" aktiv. Bitte Startknoten auf der Karte auswählen.');
    };

    return (
        <div className="bg-noc-light-dark text-noc-text rounded-lg border border-noc-border p-4 h-full flex flex-col space-y-4">
            <h3 className="text-xl font-bold mb-4">Sandbox Steuerung</h3>
            
            <div className="grid grid-cols-2 gap-2">
                <button 
                    onClick={() => setMode('addNode')} 
                    className={`flex items-center justify-center gap-2 py-2 px-3 rounded-md text-sm font-medium transition-colors ${mode === 'addNode' ? 'bg-noc-blue text-white' : 'bg-noc-border hover:bg-noc-blue'}`}
                >
                    <Plus size={16}/> Knoten
                </button>
                <button 
                    onClick={handleStartAddLink} 
                    className={`flex items-center justify-center gap-2 py-2 px-3 rounded-md text-sm font-medium transition-colors ${mode.startsWith('addLink') ? 'bg-noc-blue text-white' : 'bg-noc-border hover:bg-noc-blue'}`}
                >
                    <GitPullRequest size={16}/> Verbindung
                </button>
            </div>

            <div className="mt-2">
                <label className="block text-sm text-noc-text-secondary mb-1">Gerätetyp:</label>
                {/* KORRIGIERT: Deaktiviert das Dropdown und zeigt "Lade...", während die Daten geholt werden. */}
                <select 
                    value={selectedTemplateId} 
                    onChange={(e) => setSelectedTemplateId(e.target.value)}
                    className="w-full p-2 bg-noc-dark border border-noc-border rounded-md text-noc-text"
                    disabled={isLoading}
                >
                    {isLoading ? (
                        <option>Lade Geräte...</option>
                    ) : (
                        templates.map(template => (
                            <option key={template.id} value={template.id}>{template.name}</option>
                        ))
                    )}
                </select>
            </div>
            
            <div className="border-t border-noc-border pt-4 mt-auto space-y-2">
                <button className="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-md text-sm font-medium bg-noc-green text-white hover:bg-opacity-80">
                    <Save size={16}/> Topologie Speichern
                </button>
                <button className="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-md text-sm font-medium bg-noc-purple text-white hover:bg-opacity-80">
                    Szenario Editor
                </button>
            </div>
        </div>
    );
};

export default SandboxControlPanel;