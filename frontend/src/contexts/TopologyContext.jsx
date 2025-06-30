import React, { createContext, useState, useEffect, useCallback, useContext } from 'react';
import { AuthContext } from './AuthContext';
import L from 'leaflet';

export const TopologyContext = createContext();

export const TopologyProvider = ({ children }) => {
    const [topology, setTopology] = useState({ type: "FeatureCollection", features: [] });
    const [liveMetrics, setLiveMetrics] = useState({ current: {}, history: {} });
    const [incidents, setIncidents] = useState([]);
    const [securityEvents, setSecurityEvents] = useState([]);
    const [selectedElement, setSelectedElement] = useState(null);
    const [tracedPath, setTracedPath] = useState(null);
    const [mapBounds, setMapBounds] = useState(null);
    const { isAuthenticated, token, logout } = useContext(AuthContext);

    const fetchTopology = useCallback(async () => {
        // KORREKTUR: Führe den Fetch nur aus, wenn der Token wirklich vorhanden ist.
        if (!token) {
            console.log("Kein Token vorhanden, warte auf Login.");
            return;
        }
        try {
            const response = await fetch('/api/v1/topology/', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if(response.ok) {
                const data = await response.json();
                setTopology(data);
                if (data.features && data.features.length > 0) {
                    const bounds = L.geoJSON(data).getBounds();
                    if (bounds.isValid()) {
                        setMapBounds(bounds);
                    }
                }
            } else if (response.status === 401) {
                console.error("Auth error, logging out.");
                logout();
            }
        } catch (error) {
            console.error("Fehler beim Laden der Topologie:", error);
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
            const wsProtocol = window.location.protocol === 'https' ? 'wss' : 'ws';
            const wsUrl = `${wsProtocol}://${window.location.host}/ws/live-updates`;
            
            if (socket && (socket.readyState === WebSocket.OPEN || socket.readyState === WebSocket.CONNECTING)) {
                socket.close();
            }

            socket = new WebSocket(wsUrl);

            socket.onopen = () => console.log("WebSocket-Verbindung geöffnet.");
            socket.onclose = () => {
                console.log("WebSocket-Verbindung geschlossen. Erneuter Verbindungsversuch in 5s.");
                if (reconnectTimer) clearTimeout(reconnectTimer);
                reconnectTimer = setTimeout(connectWebSocket, 5000);
            };
            socket.onerror = (error) => console.error("WebSocket-Fehler: ", error);

            socket.onmessage = (event) => {
                try {
                    const message = JSON.parse(event.data);
                    const { type, payload } = message;

                    if (type === 'node_update') {
                        setTopology(prev => ({
                            ...prev,
                            features: prev.features.map(f => {
                                if (f.geometry.type === 'Point' && f.properties.id === payload.id) {
                                    return { ...f, properties: { ...f.properties, status: payload.status } };
                                }
                                return f;
                            })
                        }));
                        setSelectedElement(prev => (prev && prev.properties.id === payload.id ? { ...prev, properties: { ...prev.properties, status: payload.status } } : prev));
                    }
                    if (type === 'link_update') {
                        // Link-Update Logik hier (falls benötigt)
                    }
                    if (type === 'metrics_update') {
                        setLiveMetrics(prev => ({
                            current: { ...prev.current, ...payload },
                            history: Object.keys(payload).reduce((acc, nodeId) => {
                                acc[nodeId] = payload[nodeId].history;
                                return acc;
                            }, { ...prev.history })
                        }));
                    }
                    if (type === 'security_event') {
                        setSecurityEvents(prev => [payload, ...prev].slice(0, 100));
                    }
                    if (type === 'new_incident') {
                        setIncidents(prev => [payload, ...prev]);
                    }
                    if (type === 'clear_security_state') {
                        setIncidents([]);
                        setSecurityEvents([]);
                    }
                } catch (e) {
                    console.error("Fehler beim Verarbeiten der WebSocket-Nachricht:", e);
                }
            };
        };

        connectWebSocket();

        return () => {
            console.log("Bereinige WebSocket-Effekt.");
            if (reconnectTimer) {
                clearTimeout(reconnectTimer);
            }
            if (socket) {
                socket.onclose = null;
                socket.close();
            }
        };
    }, [isAuthenticated]);

    const selectElement = (element, trace = false) => {
        setSelectedElement(element);
        setTracedPath(null);
        if (trace && element?.properties?.id) {
            const path = ["core-router-1", "olt-1", element.properties.id];
            setTracedPath(path);
        }
    };

    const clearSelection = () => {
        setSelectedElement(null);
        setTracedPath(null);
    };

    const traceAndShowOnMap = (deviceId) => {
        const node = topology.features.find(f => f.properties.id === deviceId);
        if (node) {
            selectElement(node, true);
        }
    };

    const value = {
        topology, setTopology, liveMetrics, incidents, securityEvents,
        selectedElement, selectElement, clearSelection,
        tracedPath, traceAndShowOnMap, mapBounds
    };

    return <TopologyContext.Provider value={value}>{children}</TopologyContext.Provider>;
};