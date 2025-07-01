import React, { useContext } from 'react';
import { MapContainer, TileLayer, GeoJSON, Marker, useMapEvents } from 'react-leaflet';
import { renderToStaticMarkup } from 'react-dom/server';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { TopologyContext } from '../contexts/TopologyContext';
import { SandboxContext } from '../contexts/SandboxContext';
import ControlPanel from '../components/topology/ControlPanel';
import { Network, Server, Cpu, Cable, AlertCircle, GitMerge, Globe } from 'lucide-react';

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

const MapEventsHandler = ({ isSandbox }) => {
    const { selectElement } = useContext(TopologyContext);
    const sandboxCtx = useContext(SandboxContext);

    useMapEvents({
        click(e) {
            if (isSandbox && sandboxCtx?.sandboxMode === 'addNode') {
                sandboxCtx.addNode(e.latlng);
            } else {
                selectElement(null);
            }
        },
    });
    return null;
};

const TopologyPage = ({ isSandbox = false }) => {
    const { topology, selectElement, selectedElement, mapRef } = useContext(TopologyContext);
    const sandboxCtx = useContext(SandboxContext);

    const onEachFeature = (feature, layer) => {
        layer.on('click', (e) => {
            L.DomEvent.stopPropagation(e);
            if (isSandbox && sandboxCtx) {
                if (sandboxCtx.sandboxMode.startsWith('addLink')) {
                    sandboxCtx.handleLinkNodeClick(feature);
                } else {
                    selectElement(feature);
                }
            } else {
                selectElement(feature);
            }
        });
    };
    
    const styleFeature = (feature) => {
        const props = feature.properties || {};
        const isSelected = selectedElement && selectedElement.properties && selectedElement.properties.id === props.id;
        return {
            color: getStatusColor(props.status),
            weight: isSelected ? 5 : 3,
            opacity: 0.9,
        };
    };

    const pointToLayer = (feature, latlng) => {
        return L.marker(latlng, {
            icon: createDeviceIcon(feature.properties.type, feature.properties.status)
        });
    };

    return (
        <MapContainer ref={mapRef} center={[52.51, 13.42]} zoom={12} style={{ height: '100%', width: '100%' }}>
            <TileLayer url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png" attribution='© CARTO' />
            <MapEventsHandler isSandbox={isSandbox} />
            <GeoJSON
                key={JSON.stringify(topology) + JSON.stringify(selectedElement)}
                data={topology}
                style={styleFeature}
                onEachFeature={onEachFeature}
                pointToLayer={pointToLayer}
            />
        </MapContainer>
    );
};

export default TopologyPage;