import React, { createContext, useState, useEffect, useCallback, useContext, useRef } from 'react';
import { AuthContext } from './AuthContext';
import L from 'leaflet';

export const TopologyContext = createContext();

export const TopologyProvider = ({ children }) => {
    const [topology, setTopology] = useState({ type: "FeatureCollection", features: [] });
    const [liveMetrics, setLiveMetrics] = useState({ current: {}, history: {} });
    const [incidents, setIncidents] = useState([]);
    const [securityEvents, setSecurityEvents] = useState([]);
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

    useEffect(() => {
        if (!isAuthenticated) return;

        let socket;
        let reconnectTimer;

        const connectWebSocket = () => {
            const wsProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
            const wsUrl = `${wsProtocol}${window.location.host}/ws/live-updates`;
            
            socket = new WebSocket(wsUrl);

            socket.onmessage = (event) => {
                try {
                    const message = JSON.parse(event.data);
                    const { type, payload } = message;

                    if (type === 'node_update') {
                        setTopology(prev => ({
                            ...prev,
                            features: prev.features.map(f => 
                                f.properties.id === payload.id ? { ...f, properties: { ...f.properties, status: payload.status } } : f
                            )
                        }));
                    }
                    // ... other event types
                } catch (e) { console.error("WebSocket message error:", e); }
            };

            socket.onclose = () => {
                clearTimeout(reconnectTimer);
                reconnectTimer = setTimeout(connectWebSocket, 5000);
            };
        };

        connectWebSocket();

        return () => {
            clearTimeout(reconnectTimer);
            if (socket) socket.close();
        };
    }, [isAuthenticated]);

    const selectElement = (element) => setSelectedElement(element);
    const focusOnElement = (element) => {
        if (element?.geometry.type === 'Point' && mapRef.current) {
            const [lng, lat] = element.geometry.coordinates;
            mapRef.current.flyTo([lat, lng], 16);
        }
        selectElement(element);
    };

    const value = {
        topology, setTopology,
        liveMetrics, incidents, securityEvents,
        selectedElement, selectElement,
        mapRef, focusOnElement
    };

    return <TopologyContext.Provider value={value}>{children}</TopologyContext.Provider>;
};