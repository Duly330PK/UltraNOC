import React, { useContext, useMemo, useCallback } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import { TopologyContext } from '../../contexts/TopologyContext';

const ForceGraph2DComponent = () => {
    const { topology, selectElement, selectedElement } = useContext(TopologyContext);

    const graphData = useMemo(() => {
        if (!topology || !topology.features) {
            return { nodes: [], links: [] };
        }

        const nodes = topology.features
            .filter(f => f.geometry.type === 'Point')
            .map(f => ({
                id: f.properties.id,
                name: f.properties.label,
                type: f.properties.type,
                status: f.properties.status,
                val: 10 // Node size
            }));

        const links = topology.features
            .filter(f => f.geometry.type === 'LineString')
            .map(f => ({
                source: f.properties.source,
                target: f.properties.target,
                status: f.properties.status
            }));

        return { nodes, links };
    }, [topology]);

    const getStatusColor = (status) => {
        switch (status) {
            case 'online': return '#3fb950';
            case 'offline': return '#f85149';
            case 'rebooting': return '#d29922';
            default: return '#8b949e';
        }
    };
    
    const handleNodeClick = useCallback(node => {
        const feature = topology.features.find(f => f.properties.id === node.id);
        if (feature) {
            selectElement(feature);
        }
    }, [topology, selectElement]);


    const drawNode = (node, ctx) => {
        const isSelected = selectedElement && selectedElement.properties.id === node.id;
        
        // Outer glow for selected node
        if (isSelected) {
            ctx.shadowBlur = 20;
            ctx.shadowColor = '#58a6ff';
        }

        ctx.beginPath();
        ctx.arc(node.x, node.y, 8, 0, 2 * Math.PI, false);
        ctx.fillStyle = getStatusColor(node.status);
        ctx.fill();
        
        // Reset shadow for other nodes
        ctx.shadowBlur = 0;

        ctx.strokeStyle = '#fff';
        ctx.lineWidth = isSelected ? 2 : 0;
        ctx.stroke();
    };

    const drawLink = (link, ctx) => {
        ctx.lineWidth = 1.5;
        ctx.strokeStyle = getStatusColor(link.status);
    };

    return (
        <div style={{ background: '#0d1117', height: '100%', width: '100%' }}>
            <ForceGraph2D
                graphData={graphData}
                nodeCanvasObject={drawNode}
                linkCanvasObject={drawLink}
                onNodeClick={handleNodeClick}
                backgroundColor="#0d1117"
                linkColor={link => getStatusColor(link.status)}
                linkWidth={2}
            />
        </div>
    );
};

export default ForceGraph2DComponent;