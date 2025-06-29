import React, { useContext } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { TopologyContext } from '../../../contexts/TopologyContext';

const DetailRenderer = ({ data, level = 0 }) => {
    if (typeof data !== 'object' || data === null) {
        return <span className="text-noc-blue">{String(data)}</span>;
    }

    return (
        <div style={{ marginLeft: level * 12 }} className="space-y-1">
            {Object.entries(data).map(([key, value]) => (
                <div key={key}>
                    <span className="text-noc-text-secondary">{key}: </span>
                    {Array.isArray(value) ? (
                        <div className="pl-4 border-l border-noc-border">
                            {value.map((item, index) => <DetailRenderer key={index} data={item} level={level + 1} />)}
                        </div>
                    ) : typeof value === 'object' && value !== null ? (
                        <DetailRenderer data={value} level={level + 1} />
                    ) : (
                        <span className="text-noc-blue font-semibold">{String(value)}</span>
                    )}
                </div>
            ))}
        </div>
    );
};

const LiveMetricGraph = ({ data, dataKey, stroke, unit }) => (
    <ResponsiveContainer width="100%" height={80}>
        <LineChart data={data} margin={{ top: 5, right: 20, left: -10, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#30363d" />
            <XAxis dataKey="timestamp" tickFormatter={(ts) => new Date(ts).toLocaleTimeString()} stroke="#8b949e" tick={{fontSize: 10}} />
            <YAxis stroke="#8b949e" tick={{fontSize: 10}} unit={unit} domain={[0, 'dataMax + 10']}/>
            <Tooltip contentStyle={{ backgroundColor: '#161b22', border: '1px solid #30363d' }} itemStyle={{color: stroke}} labelStyle={{color: '#c9d1d9'}}/>
            <Line type="monotone" dataKey={dataKey} stroke={stroke} strokeWidth={2} dot={false} isAnimationActive={false} />
        </LineChart>
    </ResponsiveContainer>
);

const DetailsTab = ({ element }) => {
    const { liveMetrics } = useContext(TopologyContext);
    const elementId = element.properties.id;
    const metricsHistory = liveMetrics.history[elementId] || [];
    const isNode = element.geometry.type === 'Point';

    return (
        <div className="text-sm font-mono whitespace-pre-wrap">
            {isNode && element.properties.type !== 'Muffe' && (
                <div className="mb-4 p-3 bg-noc-dark rounded-md border border-noc-border">
                   <h4 className="text-md text-noc-text-secondary mb-2 font-sans font-bold">Live Metriken</h4>
                   <div>CPU Auslastung (%)</div>
                   <LiveMetricGraph data={metricsHistory} dataKey="cpu" stroke="#58a6ff" unit="%" />
                   <div>Temperatur (°C)</div>
                   <LiveMetricGraph data={metricsHistory} dataKey="temp" stroke="#d29922" unit="°C" />
                </div>
            )}
            <h4 className="text-md text-noc-text-secondary mt-4 mb-2 font-sans font-bold">Eigenschaften</h4>
            <div className="p-3 bg-noc-dark rounded-md border border-noc-border">
                <DetailRenderer data={element.properties} />
            </div>
        </div>
    );
};

export default DetailsTab;