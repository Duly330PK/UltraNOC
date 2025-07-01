import React, { useContext, useCallback } from 'react';
import { MapContainer, TileLayer, GeoJSON, Marker, useMapEvents } from 'react-leaflet';
import { renderToStaticMarkup } from 'react-dom/server';
import L from 'leaflet';
import { TopologyContext } from '../../contexts/TopologyContext';
import { SandboxContext } from '../../contexts/SandboxContext';
import { Network, Server, Cpu, Cable, AlertCircle, GitMerge, Globe } from 'lucide-react';

// --- Icon Logic (copied for encapsulation) ---
const getIconForType = (type) => {
    if (!type) return <AlertCircle size={16} />;
    if (type.includes('MPLS Core Router')) return <Globe size={16} />;
    if (type.includes('Broadband Network Gateway')) return <Server size={16} />;
    if (type.includes('Aggregation Switch')) return <GitMerge size={16} />;
    if (type.includes('OLT')) return <Cpu size={16} />;
    if (type.includes('Muffe') || type.includes('Splitter')) return <Cable size={16} />;
    if (type.includes('ONT')) return <Network size={16} />;
    return <AlertCircle size={16} />;
};

const getStatusColor = (status) => {
    switch (status) {
        case 'online': return '#3fb950';
        case 'offline': return '#f85149';
        case 'rebooting': case 'warning': return '#d29922';
        default: return '#8b949e';
    }
};

const createDeviceIcon = (type, status) => {
    const iconMarkup = renderToStaticMarkup(
        <div className="relative flex items-center justify-center w-8 h-8">
            <div className="absolute w-full h-full rounded-full opacity-30" style={{ backgroundColor: getStatusColor(status) }}></div>
            <div className="absolute flex items-center justify-center w-6 h-6 rounded-full bg-noc-light-dark border" style={{ borderColor: getStatusColor(status) }}>
                {getIconForType(type)}
            </div>
        </div>
    );
    return L.divIcon({ html: iconMarkup, className: 'custom-leaflet-icon', iconSize: [32, 32], iconAnchor: [16, 16] });
};

// --- Map Interaction Component ---
const MapEventsController = () => {
    const { addNode, addLink, sandboxMode, setSandboxMode } = useContext(SandboxContext);
    const { selectElement } = useContext(TopologyContext);

    useMapEvents({
        click(e) {
            if (sandboxMode === 'addNode') {
                addNode(e.latlng);
            } else {
                selectElement(null); // Deselect on map click
            }
        },
    });

    return null;
};


const SandboxMap = () => {
    const { topology, selectedElement, selectElement } = useContext(TopologyContext);
    const { sandboxMode, handleNodeClickForLink } = useContext(SandboxContext);

    const onEachFeature = (feature, layer) => {
        if (feature.geometry.type === "Point") {
            layer.on('click', (e) => {
                L.DomEvent.stopPropagation(e);
                if (sandboxMode === 'addLinkStart' || sandboxMode === 'addLinkEnd') {
                    handleNodeClickForLink(feature);
                } else {
                    selectElement(feature);
                }
            });
        }
    };
    
    const styleFeature = (feature) => ({
        color: getStatusColor(feature.properties.status),
        weight: 3,
        opacity: 0.9
    });

    const pointToLayer = (feature, latlng) => L.marker(latlng, {
        icon: createDeviceIcon(feature.properties.type, feature.properties.status)
    });

    return (
        <MapContainer center={[52.51, 13.42]} zoom={12} style={{ height: '100%', width: '100%' }}>
            <TileLayer url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png" />
            <MapEventsController />
            <GeoJSON
                key={JSON.stringify(topology)}
                data={topology}
                style={styleFeature}
                onEachFeature={onEachFeature}
                pointToLayer={pointToLayer}
            />
        </MapContainer>
    );
};

export default SandboxMap;