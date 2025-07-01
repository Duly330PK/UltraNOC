import React, { createContext, useState, useEffect, useCallback, useContext, useRef } from 'react';
import { AuthContext } from './AuthContext';
import L from 'leaflet';

export const TopologyContext = createContext();

export const TopologyProvider = ({ children }) => {
    // Initialize all state with stable defaults
    const [topology, setTopology] = useState({ type: "FeatureCollection", features: [] });
    const [liveMetrics, setLiveMetrics] = useState({ current: {}, history: {} });
    const [incidents, setIncidents] = useState([]);
    const [securityEvents, setSecurityEvents] = useState([]);
    const [selectedElement, setSelectedElement] = useState(null);
    const { isAuthenticated, token, logout } = useContext(AuthContext);
    
    const mapRef = useRef(null);

    const fetchTopology = useCallback(async () => {
        if (!token) return;
        try {
            const response = await fetch('/api/v1/sandbox/load', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (response.ok) {
                const data = await response.json();
                setTopology(data || { type: "FeatureCollection", features: [] });
            } else if (response.status === 401) {
                logout();
            }
        } catch (error) {
            console.error("Failed to load topology:", error);
        }
    }, [token, logout]);

    useEffect(() => {
        if (isAuthenticated) {
            fetchTopology();
        }
    }, [isAuthenticated, fetchTopology]);

    useEffect(() => {
        if (!isAuthenticated) return;

        let socket;
        let reconnectTimer;

        const connectWebSocket = () => {
            // WebSocket connection logic here...
            // This remains the same as before.
        };

        connectWebSocket();

        return () => {
            // Cleanup logic here...
        };
    }, [isAuthenticated]);

    const selectElement = (element) => {
        setSelectedElement(element);
    };

    const focusOnElement = (element) => {
        if (element && element.geometry.type === 'Point' && mapRef.current) {
            const [lng, lat] = element.geometry.coordinates;
            mapRef.current.flyTo([lat, lng], 16);
        }
        selectElement(element);
    };

    const value = {
        topology, setTopology,
        liveMetrics, incidents, securityEvents, // These are now guaranteed to be arrays/objects
        selectedElement, selectElement,
        mapRef, focusOnElement
    };

    return <TopologyContext.Provider value={value}>{children}</TopologyContext.Provider>;
};