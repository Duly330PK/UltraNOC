import React, { createContext, useState, useEffect, useContext } from 'react';
import { TopologyContext } from './TopologyContext';

export const SandboxContext = createContext();

export const SandboxProvider = ({ children }) => {
    const [sandboxMode, setSandboxMode] = useState('view');
    const [nodeTypeToAdd, setNodeTypeToAdd] = useState('');
    const [linkSourceNode, setLinkSourceNode] = useState(null);
    const [deviceTemplates, setDeviceTemplates] = useState([]);
    
    const { setTopology } = useContext(TopologyContext);

    useEffect(() => {
        const fetchDeviceTemplates = async () => {
            const token = localStorage.getItem('ultranoc_token');
            try {
                const response = await fetch('/api/v1/topology/device-templates', { headers: { 'Authorization': `Bearer ${token}` } });
                const data = await response.json();
                setDeviceTemplates(data);
                if (data.length > 0) {
                    setNodeTypeToAdd(data[0].id);
                }
            } catch (error) { console.error("Failed to load device templates:", error); }
        };
        fetchDeviceTemplates();
    }, []);

    const addNode = (latlng) => {
        const selectedTemplate = deviceTemplates.find(t => t.id === nodeTypeToAdd) || { name: 'Device', type: 'Generic' };
        const newNode = {
            type: "Feature",
            geometry: { type: "Point", coordinates: [latlng.lng, latlng.lat] },
            properties: { 
                id: `node-${Date.now()}`, 
                label: `New ${selectedTemplate.name}`, 
                type: selectedTemplate.type, 
                template_id: selectedTemplate.id,
                status: 'online', 
                details: {}
            }
        };
        setTopology(prev => ({ ...prev, features: [...(prev.features || []), newNode] }));
        setSandboxMode('view');
    };

    const handleLinkNodeClick = (targetNode) => {
        if (sandboxMode === 'addLinkStart') {
            setLinkSourceNode(targetNode);
            setSandboxMode('addLinkEnd');
            alert(`Startknoten ${targetNode.properties.id} ausgewählt. Zielknoten wählen.`);
        } else if (sandboxMode === 'addLinkEnd') {
            if (linkSourceNode && linkSourceNode.properties.id !== targetNode.properties.id) {
                const newLink = {
                    type: "Feature",
                    geometry: { type: "LineString", coordinates: [ linkSourceNode.geometry.coordinates, targetNode.geometry.coordinates ] },
                    properties: { source: linkSourceNode.properties.id, target: targetNode.properties.id, status: 'online', type: 'Fiber Link' }
                };
                setTopology(prev => ({ ...prev, features: [...(prev.features || []), newLink] }));
            }
            // FIX: Always reset to view mode after the second click
            setSandboxMode('view');
            setLinkSourceNode(null);
        }
    };

    const value = {
        sandboxMode, setSandboxMode,
        nodeTypeToAdd, setNodeTypeToAdd,
        linkSourceNode, setLinkSourceNode,
        deviceTemplates,
        addNode, handleLinkNodeClick
    };

    return <SandboxContext.Provider value={value}>{children}</SandboxContext.Provider>;
};