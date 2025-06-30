import React, { useContext, useEffect, useState, useRef } from 'react';
import { TopologyContext } from '../contexts/TopologyContext';
// KORREKTUR: Import mit geschweiften Klammern, da es kein Default-Export ist.
import { ForceGraph3D } from 'react-force-graph';

const Topology3DPage = () => {
    const { topology, selectElement } = useContext(TopologyContext);
    const [graphData, setGraphData] = useState({ nodes: [], links: [] });
    const fgRef = useRef();

    // Transform GeoJSON data to graph data format { nodes, links }
    useEffect(() => {
        if (topology && topology.features) {
            const nodes = topology.features
                .filter(f => f.geometry.type === 'Point')
                .map(f => ({
                    id: f.properties.id,
                    label: f.properties.label,
                    type: f.properties.type,
                    status: f.properties.status,
                    feature: f // Keep original feature for click events
                }));

            const links = topology.features
                .filter(f => f.geometry.type === 'LineString')
                .map(f => ({
                    source: f.properties.source,
                    target: f.properties.target,
                    status: f.properties.status
                }));
            
            setGraphData({ nodes, links });
        }
    }, [topology]);

    const getNodeColor = (node) => {
        switch (node.status) {
            case 'online': return '#3fb950';
            case 'offline': return '#f85149';
            case 'rebooting': return '#d29922';
            default: return '#8b949e';
        }
    };

    const handleNodeClick = (node) => {
        // Center camera on node
        const distance = 40;
        const distRatio = 1 + distance/Math.hypot(node.x, node.y, node.z);
        if (fgRef.current) {
            fgRef.current.cameraPosition(
                { x: node.x * distRatio, y: node.y * distRatio, z: node.z * distRatio }, // new position
                node, // lookAt target
                3000  // ms transition duration
            );
        }
        // Select element in the control panel
        if (selectElement && node.feature) {
            selectElement(node.feature);
        }
    };

    // This is crucial to prevent SSR issues with 3D libraries
    const [isClient, setIsClient] = useState(false);
    useEffect(() => {
        setIsClient(true);
    }, []);

    if (!isClient) {
        return null; // Render nothing on the server
    }

    return (
        <div style={{ width: '100%', height: '100%', backgroundColor: '#0d1117' }}>
            <ForceGraph3D
                ref={fgRef}
                graphData={graphData}
                nodeLabel="label"
                nodeAutoColorBy="type"
                nodeColor={getNodeColor}
                linkColor={() => 'rgba(255,255,255,0.2)'}
                linkWidth={0.5}
                backgroundColor="#0d1117"
                onNodeClick={handleNodeClick}
            />
        </div>
    );
};

export default Topology3DPage;