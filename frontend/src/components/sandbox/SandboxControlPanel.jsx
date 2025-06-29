import React, { useState, useContext, useEffect } from 'react';
import { TopologyContext } from '../../contexts/TopologyContext';
import { MapPin, Router, Link, GitPullRequest, Save, FolderOpen, Plus, Settings } from 'lucide-react';

// Eine einfache Gerätedatenbank für den Sandbox-Modus
const deviceTemplates = [
    { id: 'new-router', label: 'Neuer Router', type: 'Core Router', details: { ip_address: '0.0.0.0', firmware: { os: 'Generic OS', version: '1.0' }}},
    { id: 'new-olt', label: 'Neue OLT', type: 'OLT', details: { active_onts: 0 }},
    { id: 'new-muffe', label: 'Neue Muffe', type: 'Muffe', details: { fiber_type: 'SMF' }},
    { id: 'new-ont', label: 'Neues ONT', type: 'ONT', details: { rx_power_dbm: -25.0 }}
];

const SandboxControlPanel = () => {
    const { topology, setTopology } = useContext(TopologyContext);
    const [mode, setMode] = useState('view'); // 'view', 'addNode', 'addLink'
    const [selectedNodeType, setSelectedNodeType] = useState(deviceTemplates[0].id);
    const [selectedLinkSource, setSelectedLinkSource] = useState(null);

    const handleAddNode = () => {
        setMode('addNode');
        alert('Klicken Sie auf die Karte, um einen neuen Knoten zu platzieren.');
    };

    const handleMapClick = (e) => {
        if (mode === 'addNode') {
            const newId = `node-${Date.now()}`;
            const newDeviceTemplate = deviceTemplates.find(t => t.id === selectedNodeType);
            const newNode = {
                type: "Feature",
                geometry: { type: "Point", coordinates: [e.latlng.lng, e.latlng.lat] },
                properties: { 
                    id: newId, 
                    label: newDeviceTemplate.label, 
                    type: newDeviceTemplate.type, 
                    status: 'online', 
                    details: newDeviceTemplate.details 
                }
            };
            setTopology(prev => ({
                ...prev,
                features: [...prev.features, newNode]
            }));
            setMode('view');
        } else if (mode === 'addLink' && selectedLinkSource) {
            // Implement link creation logic in ControlPanel or directly in MapView
            // For now, this is handled via an interaction in MapView
            setSelectedLinkSource(null); // Reset after potential link creation attempt
        }
    };

    const handleAddLink = () => {
        setMode('addLink');
        setSelectedLinkSource(null);
        alert('Klicken Sie auf den ersten Knoten für die Verbindung.');
    };

    const handleNodeClickForLink = (nodeId) => {
        if (mode === 'addLink') {
            if (!selectedLinkSource) {
                setSelectedLinkSource(nodeId);
                alert(`Erster Knoten ausgewählt: ${nodeId}. Klicken Sie auf den zweiten Knoten.`);
            } else {
                const newLink = {
                    type: "Feature",
                    geometry: { type: "LineString", coordinates: [] }, // Koordinaten werden vom MapView gesetzt
                    properties: {
                        source: selectedLinkSource,
                        target: nodeId,
                        status: 'online',
                        type: 'Fiber Link',
                        length_km: 1.0, // Standardwert, später editierbar
                    }
                };
                setTopology(prev => ({
                    ...prev,
                    features: [...prev.features, newLink]
                }));
                setMode('view');
                setSelectedLinkSource(null);
            }
        }
    };

    return (
        <div className="bg-noc-light-dark text-noc-text rounded-lg border border-noc-border p-4 h-full flex flex-col space-y-4">
            <h3 className="text-xl font-bold mb-4">Sandbox Steuerung</h3>

            {/* Modus-Auswahl */}
            <div className="grid grid-cols-2 gap-2">
                <button 
                    onClick={handleAddNode} 
                    className={`flex items-center justify-center gap-2 py-2 px-3 rounded-md text-sm font-medium transition-colors ${mode === 'addNode' ? 'bg-noc-blue text-white' : 'bg-noc-border hover:bg-noc-blue hover:text-white'}`}
                >
                    <Plus size={16}/> Knoten hinzufügen
                </button>
                <button 
                    onClick={handleAddLink} 
                    className={`flex items-center justify-center gap-2 py-2 px-3 rounded-md text-sm font-medium transition-colors ${mode === 'addLink' ? 'bg-noc-blue text-white' : 'bg-noc-border hover:bg-noc-blue hover:text-white'}`}
                >
                    <GitPullRequest size={16}/> Link zeichnen
                </button>
            </div>

            {mode === 'addNode' && (
                <div className="mt-2">
                    <label className="block text-sm text-noc-text-secondary mb-1">Gerätetyp:</label>
                    <select 
                        value={selectedNodeType} 
                        onChange={(e) => setSelectedNodeType(e.target.value)}
                        className="w-full p-2 bg-noc-dark border border-noc-border rounded-md text-noc-text"
                    >
                        {deviceTemplates.map(template => (
                            <option key={template.id} value={template.id}>{template.label}</option>
                        ))}
                    </select>
                </div>
            )}

            {/* Separator */}
            <div className="border-t border-noc-border pt-4 mt-4"></div>

            {/* Allgemeine Aktionen */}
            <div className="flex flex-col space-y-2">
                <button className="flex items-center gap-2 py-2 px-3 rounded-md text-sm font-medium bg-noc-green hover:bg-opacity-80 text-white">
                    <Save size={16}/> Topologie Speichern
                </button>
                <button className="flex items-center gap-2 py-2 px-3 rounded-md text-sm font-medium bg-noc-blue hover:bg-opacity-80 text-white">
                    <FolderOpen size={16}/> Topologie Laden
                </button>
                <button className="flex items-center gap-2 py-2 px-3 rounded-md text-sm font-medium bg-noc-purple hover:bg-opacity-80 text-white">
                    <Settings size={16}/> Szenario Editor
                </button>
            </div>
        </div>
    );
};

export default SandboxControlPanel;