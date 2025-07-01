import React, { createContext, useState, useEffect, useCallback, useContext, useRef } from 'react';
import { AuthContext } from './AuthContext';

export const TopologyContext = createContext();

export const TopologyProvider = ({ children }) => {
    const [topology, setTopology] = useState({ type: "FeatureCollection", features: [] });
    const [selectedElement, setSelectedElement] = useState(null);
    const [focusedElement, setFocusedElement] = useState(null);
    const { isAuthenticated, token, logout } = useContext(AuthContext);
    
    const mapRef = useRef(null);

    const fetchTopology = useCallback(async () => {
        if (!token) return;
        try {
            const response = await fetch('/api/v1/sandbox/load', { headers: { 'Authorization': `Bearer ${token}` } });
            if (response.ok) {
                setTopology(await response.json() || { type: "FeatureCollection", features: [] });
            } else if (response.status === 401) {
                logout();
            }
        } catch (error) { console.error("Failed to load topology:", error); }
    }, [token, logout]);

    useEffect(() => { if (isAuthenticated) fetchTopology(); }, [isAuthenticated, fetchTopology]);

    const selectElement = (element) => {
        setSelectedElement(element);
    };

    const focusOnElement = (element) => {
        if (element?.geometry.type === 'Point' && mapRef.current) {
            const [lng, lat] = element.geometry.coordinates;
            mapRef.current.flyTo([lat, lng], 16);
        }
        selectElement(element);
    };
    
    // NEW: Function to delete a specific element and its connected links
    const deleteElement = (elementId) => {
        setTopology(prev => {
            // Remove the node itself
            const newFeatures = prev.features.filter(f => f.properties.id !== elementId);
            // Remove any links connected to the node
            const finalFeatures = newFeatures.filter(f => 
                f.geometry.type !== 'LineString' || 
                (f.properties.source !== elementId && f.properties.target !== elementId)
            );
            return { ...prev, features: finalFeatures };
        });
        setSelectedElement(null); // Deselect after deletion
    };

    // NEW: Function to clear the entire sandbox
    const clearTopology = () => {
        setTopology({ type: "FeatureCollection", features: [] });
        setSelectedElement(null);
    };

    const value = {
        topology, setTopology,
        selectedElement, selectElement,
        focusedElement, focusOnElement,
        mapRef,
        deleteElement, // Expose the new delete function
        clearTopology  // Expose the new clear function
    };

    return <TopologyContext.Provider value={value}>{children}</TopologyContext.Provider>;
};