import React, { useState, useEffect, useCallback, useContext } from 'react';
import { MapContainer, TileLayer, Marker, Polyline, useMapEvents, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { TopologyContext } from '../../contexts/TopologyContext';
import DevicePropertiesPanel from '../sandbox/DevicePropertiesPanel';

// Leaflet Icon Fix (Vite)
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
    iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

const getStatusColor = (status) => {
    switch (status) {
        case 'online': return '#3fb950';
        case 'offline': return '#f85149';
        case 'rebooting':
        case 'updating':
        case 'maintenance':
        case 'warning': return '#d29922';
        default: return '#8b949e';
    }
};

const LeafletMap = () => {
    // =================================================================
    // HIER IST DIE EINZIGE ÄNDERUNG: 'selectedElement' wurde hinzugefügt
    // =================================================================
    const { topology, selectedElement, selectElement, clearSelection, tracedPath, mapBounds, setTopology } = useContext(TopologyContext);
    const [isAddingLink, setIsAddingLink] = useState(false);
    const [newLinkSource, setNewLinkSource] = useState(null);
    const [selectedForLink, setSelectedForLink] = useState(null);
    const [showProperties, setShowProperties] = useState(false);

    const handleMapClick = (e) => {
        if (isAddingLink) {
            if (selectedForLink) {
                // Erstelle neuen Link im Zustand
                setTopology(prev => {
                    const newLink = {
                        type: "Feature",
                        geometry: { type: "LineString", coordinates: [ [selectedForLink.geometry.coordinates[0], selectedForLink.geometry.coordinates[1]], [e.latlng.lng, e.latlng.lat] ] },
                        properties: {
                            source: selectedForLink.properties.id,
                            target: `new-node-${Date.now()}`,
                            status: 'online',
                            type: 'Fiber Link',
                            length_km: 1.0,
                        }
                    };
                    return { ...prev, features: [...prev.features, newLink] };
                });
                setIsAddingLink(false);
                setSelectedForLink(null);
            }
            else {
                alert("Bitte wähle zuerst einen Startknoten aus.");
            }
        }
    };

    const handleNodeClick = (feature) => {
        if(isAddingLink) {
            setSelectedForLink(feature);
            alert("Knoten für Verbindung ausgewählt. Klicken Sie auf einen zweiten Knoten.")
        } else {
            selectElement(feature);
            setShowProperties(true);
        }
    };

    const handleCloseProperties = () => {
        setShowProperties(false);
        clearSelection();
    };

    const styleFeature = (feature) => {
        const isSelected = selectedElement?.properties?.id === feature.properties.id;
        const isLinkSelected = selectedElement?.properties?.source === feature.properties.source && selectedElement?.properties?.target === feature.properties.target;
        const inPath = tracedPath && (
            (feature.properties.id && tracedPath.includes(feature.properties.id)) || 
            (feature.properties.source && tracedPath.includes(feature.properties.source) && tracedPath.includes(feature.properties.target))
        );

        const baseStyle = getStatusColor(feature.properties.status);
        let style = { color: baseStyle, weight: 3, opacity: 0.9, fillOpacity: 0.8, fillColor: baseStyle, dashArray: null };

        if (isSelected || isLinkSelected) {
            style.weight = 5;
            style.color = '#58a6ff';
        }
        if (inPath) {
            style.weight = 5;
            style.color = '#a371f7';
            style.dashArray = '10, 5';
        }
        return style;
    };

    const pointToLayer = (feature, latlng) => {
         return L.circleMarker(latlng, {
            ...styleFeature(feature),
            radius: 8,
         });
    };

    const AddLinkControl = () => {
        const map = useMap();
        useEffect(() => {
            if (isAddingLink) {
                map.getContainer().style.cursor = 'crosshair';
            } else {
                map.getContainer().style.cursor = '';
            }
            return () => {
                map.getContainer().style.cursor = '';
            };
        }, [map, isAddingLink]);
        return null;
    };

    const MapEvents = () => {
        useMapEvents({
            click: handleMapClick
        });
        return null;
    };

    return (
        <div className="flex h-full w-full">
            <div className="flex-grow h-full relative">
                <MapContainer center={[51.9607, 7.6261]} zoom={13} style={{ height: '60vh', width: '100%' }}>
                    <TileLayer
                        attribution='© <a href="https://carto.com/attributions">CARTO</a>'
                        url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                    />
                    {topology.features && topology.features.map((feature, index) => (
                        feature.geometry.type === "Point" ? (
                            <Marker
                                key={index}
                                position={[feature.geometry.coordinates[1], feature.geometry.coordinates[0]]}
                                icon={L.divIcon({ className: 'custom-icon', html: `<span style="color:${getStatusColor(feature.properties.status)}">●</span>` })}
                                eventHandlers={{ click: () => handleNodeClick(feature) }}
                            />
                        ) : (
                            <Polyline
                                key={index}
                                positions={[
                                    [feature.geometry.coordinates[0][1], feature.geometry.coordinates[0][0]],
                                    [feature.geometry.coordinates[1][1], feature.geometry.coordinates[1][0]]
                                ]}
                                style={styleFeature(feature)}
                            />
                        )
                    ))}
                    <MapEvents />
                    <AddLinkControl/>
                </MapContainer>
            </div>
            {selectedElement && showProperties && (
                <div className="w-96 h-full flex-shrink-0">
                    <DevicePropertiesPanel device={selectedElement} onClose={handleCloseProperties} />
                </div>
            )}
        </div>
    );
};

export default LeafletMap;