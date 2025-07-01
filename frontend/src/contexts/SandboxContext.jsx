import React, { createContext, useState, useEffect } from 'react';

export const SandboxContext = createContext();

export const SandboxProvider = ({ children }) => {
    const [sandboxMode, setSandboxMode] = useState('view');
    const [linkSourceNode, setLinkSourceNode] = useState(null);
    const [deviceTemplates, setDeviceTemplates] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [selectedTemplateId, setSelectedTemplateId] = useState('');
    const [topology, setTopology] = useState({ type: "FeatureCollection", features: [] });

    useEffect(() => {
        const fetchDeviceTemplates = async () => {
            setIsLoading(true);
            const token = localStorage.getItem('ultranoc_token');
            try {
                const response = await fetch('/api/v1/topology/device-templates', {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (!response.ok) throw new Error('Failed to fetch templates');
                const data = await response.json();
                setDeviceTemplates(data);
                if (data.length > 0) {
                    setSelectedTemplateId(data[0].id);
                }
            } catch (error) {
                console.error("Error loading device templates for sandbox:", error);
            } finally {
                setIsLoading(false);
            }
        };
        fetchDeviceTemplates();
    }, []);

    const value = {
        sandboxMode,
        setSandboxMode,
        linkSourceNode,
        setLinkSourceNode,
        deviceTemplates,
        isLoading,
        selectedTemplateId, 
        setSelectedTemplateId, // KORRIGIERT: Diese Funktion wird jetzt bereitgestellt
        topology,
        setTopology
    };

    return (
        <SandboxContext.Provider value={value}>
            {children}
        </SandboxContext.Provider>
    );
};