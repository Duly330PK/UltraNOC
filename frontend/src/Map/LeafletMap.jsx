import React, { useContext, useEffect, useMemo } from 'react';
import { MapContainer, TileLayer, GeoJSON, Tooltip, useMap, useMapEvents } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { TopologyContext } from '../../contexts/TopologyContext';
import { SandboxContext } from '../../contexts/SandboxContext';

// Icon Fix und Farb-Logik
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
        case 'rebooting': case 'updating': case 'maintenance': case 'warning': return '#d29922';
        default: return '#8b949e';
    }
};

const MapController = ({ bounds }) => {
    const map = useMap();
    useEffect(() => {
        if (bounds && bounds.isValid()) {
            map.fitBounds(bounds, { padding: [50, 50] });
        }
    }, [map, bounds]);
    return null;
};

const LeafletMap = ({ isSandbox = false }) => {
    const { topology, setTopology, selectedElement, selectElement, mapBounds, tracedPath } = useContext(TopologyContext);
    const sandboxContext = useContext(SandboxContext);

    const handleMapClick = (e) => {
        if (isSandbox && sandboxContext?.sandboxMode === 'addNode') {
            const { nodeTypeToAdd, setSandboxMode, deviceTemplates } = sandboxContext;
            const template = deviceTemplates.find(t => t.id === nodeTypeToAdd);
            if (!template) return;

            const newId = `${template.id}-${Date.now()}`;
            const newNode = {
                type: "Feature",
                geometry: { type: "Point", coordinates: [e.latlng.lng, e.latlng.lat] },
                properties: { id: newId, label: `Neues ${template.name}`, type: template.type, status: 'online', details: template.details, template_id: template.id }
            };
            setTopology(prev => ({ ...prev, features: [...prev.features, newNode] }));
            setSandboxMode('view');
        }
    };

    const handleNodeClick = (e, feature) => {
        L.DomEvent.stopPropagation(e);
        if (isSandbox && sandboxContext?.sandboxMode.startsWith('addLink')) {
            const { sandboxMode, setSandboxMode, linkSourceNode, setLinkSourceNode } = sandboxContext;
            if (sandboxMode === 'addLinkStart') {
                setLinkSourceNode(feature);
                setSandboxMode('addLinkEnd');
                alert(`Startknoten ${feature.properties.id} ausgewählt. Wählen Sie den Zielknoten.`);
            } else if (sandboxMode === 'addLinkEnd' && linkSourceNode) {
                const newLink = {
                    type: "Feature",
                    geometry: { "type": "LineString", "coordinates": [ linkSourceNode.geometry.coordinates, feature.geometry.coordinates ] },
                    properties: { source: linkSourceNode.properties.id, target: feature.properties.id, status: 'online', type: 'Fiber Link' }
                };
                setTopology(prev => ({ ...prev, features: [...prev.features, newLink] }));
                setSandboxMode('view');
                setLinkSourceNode(null);
            }
        } else {
            selectElement(feature);
        }
    };
    
    const onEachFeature = (feature, layer) => {
        if (feature.geometry.type === "Point") {
            layer.on({ click: (e) => handleNodeClick(e, feature) });
        } else {
             layer.on({ click: (e) => { L.DomEvent.stopPropagation(e); selectElement(feature); } });
        }
        if (feature.properties?.label) {
            layer.bindTooltip(`<b>${feature.properties.label}</b><br>${feature.properties.type}`);
        }
    };
    
    const styleFeature = (feature) => {
        const props = feature.properties;
        const isSelected = selectedElement?.properties?.id === props.id || (selectedElement?.properties?.source === props.source && selectedElement?.properties?.target === props.target);
        let inPath = false;
        if (tracedPath && props.id) { inPath = tracedPath.includes(props.id); }
        if (tracedPath && props.source) {
             for (let i = 0; i < tracedPath.length - 1; i++) {
                if ((tracedPath[i] === props.source && tracedPath[i+1] === props.target) || (tracedPath[i] === props.target && tracedPath[i+1] === props.source)) {
                    inPath = true; break;
                }
            }
        }

        const baseStyle = getStatusColor(props.status);
        let style = { color: baseStyle, weight: 3, opacity: 0.9, fillOpacity: 0.7, fillColor: baseStyle };
        if (isSelected) { style.weight = 5; style.color = '#58a6ff'; }
        if (inPath) { style.weight = 6; style.color = '#a371f7'; style.dashArray = '10, 5'; }
        return style;
    };

    const pointToLayer = (feature, latlng) => L.circleMarker(latlng, { ...styleFeature(feature), radius: 8 });

    const MapEvents = () => {
        useMapEvents({ click: handleMapClick });
        return null;
    };

    const memoizedGeoJSON = useMemo(() => (
        <GeoJSON data={topology} onEachFeature={onEachFeature} pointToLayer={pointToLayer} style={styleFeature} key={JSON.stringify(topology)} />
    ), [topology, selectedElement, tracedPath, sandboxContext?.sandboxMode]);

    return (
        <MapContainer center={[51.96, 7.62]} zoom={13} style={{ height: '100%', width: '100%' }}>
            <TileLayer url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png" attribution='© CARTO' />
            {topology.features.length > 0 && memoizedGeoJSON}
            <MapController bounds={mapBounds} />
            {isSandbox && <MapEvents />}
        </MapContainer>
    );
};

export default LeafletMap;