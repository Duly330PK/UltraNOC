import React, { useContext, useEffect, useMemo } from 'react';
import { MapContainer, TileLayer, GeoJSON, Tooltip, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { TopologyContext } from '../contexts/TopologyContext';
import ControlPanel from '../components/topology/ControlPanel';

// Leaflet Icon Fix für Vite
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

const MapController = ({ bounds }) => {
    const map = useMap();
    useEffect(() => {
        if (bounds && bounds.isValid()) {
            map.fitBounds(bounds, { padding: [50, 50] });
        }
    }, [map, bounds]);
    return null;
}

const TopologyPage = () => {
    const { topology, selectedElement, selectElement, mapBounds, tracedPath } = useContext(TopologyContext);

    const onEachFeature = (feature, layer) => {
        layer.on({ click: (e) => { L.DomEvent.stopPropagation(e); selectElement(feature); } });
        if(feature.properties?.label) {
            layer.bindTooltip(`<b>${feature.properties.label}</b><br>${feature.properties.type}`);
        }
    };

    const styleFeature = (feature) => {
        const props = feature.properties;
        const isNodeSelected = selectedElement?.geometry.type === 'Point' && selectedElement.properties.id === props.id;
        const isLinkSelected = selectedElement?.geometry.type === 'LineString' && selectedElement.properties.source === props.source && selectedElement.properties.target === props.target;

        // Prüft, ob ein Knoten oder ein Link Teil des getracten Pfades ist
        let inPath = false;
        if (tracedPath) {
            if (props.id) { // Es ist ein Knoten
                inPath = tracedPath.includes(props.id);
            } else if (props.source && props.target) { // Es ist ein Link
                for (let i = 0; i < tracedPath.length - 1; i++) {
                    if ((tracedPath[i] === props.source && tracedPath[i+1] === props.target) || (tracedPath[i] === props.target && tracedPath[i+1] === props.source)) {
                        inPath = true;
                        break;
                    }
                }
            }
        }

        // KORREKTUR HIER: 'getStatusStyle' wurde zu 'getStatusColor' geändert.
        const baseStyle = getStatusColor(props.status);
        let style = { color: baseStyle, weight: 3, opacity: 0.9, fillOpacity: 0.8, fillColor: baseStyle };

        if (isNodeSelected || isLinkSelected) {
            style.weight = 5;
            style.color = '#58a6ff';
        }
        if (inPath) {
            style.weight = 6;
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

    const memoizedGeoJSON = useMemo(() => (
        <GeoJSON 
            data={topology} 
            onEachFeature={onEachFeature} 
            pointToLayer={pointToLayer}
            style={styleFeature}
            key={JSON.stringify(topology.features.map(f => f.properties.status))}
        />
    ), [topology, selectedElement, tracedPath]);

    return (
        <div className="flex h-full w-full">
            <div className="flex-grow h-full">
                <MapContainer center={[51.9607, 7.6261]} zoom={13} style={{ height: '100%', width: '100%' }}>
                    <TileLayer
                        attribution='© <a href="https://carto.com/attributions">CARTO</a>'
                        url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                    />
                    {topology.features.length > 0 && memoizedGeoJSON}
                     <MapController bounds={mapBounds} />
                </MapContainer>
            </div>
            <div className="w-96 h-full flex-shrink-0">
                <ControlPanel />
            </div>
        </div>
    );
};

export default TopologyPage;