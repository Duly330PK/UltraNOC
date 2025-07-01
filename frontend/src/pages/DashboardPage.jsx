import React, { useContext } from 'react';
import { TopologyContext } from '../contexts/TopologyContext';
import { AlertCircle, CheckCircle, ShieldAlert, Server, Cpu } from 'lucide-react';
import ScenarioControl from '../components/dashboard/ScenarioControl';
import SecurityControl from '../components/dashboard/SecurityControl';

const StatCard = ({ label, value, color, icon }) => (
    <div className="bg-noc-light-dark p-6 rounded-lg border border-noc-border transition-all hover:border-noc-blue hover:shadow-lg">
        <div className="flex items-center gap-4">
            <div className={`p-3 rounded-full bg-opacity-10 ${color}`}>{icon}</div>
            <div>
                <h3 className="text-sm font-medium text-noc-text-secondary">{label}</h3>
                <p className={`text-3xl font-semibold mt-1 text-noc-text`}>{value}</p>
            </div>
        </div>
    </div>
);

const DashboardPage = () => {
    // FIX: Add ultra-robust guards to prevent any crashes from undefined or intermediate state data
    const { incidents = [], securityEvents = [], topology = {}, liveMetrics = {} } = useContext(TopologyContext);

    const pointFeatures = topology?.features?.filter(f => f.geometry?.type === 'Point') || [];
    const onlineDevices = pointFeatures.filter(f => f.properties?.status === 'online').length;
    const totalDevices = pointFeatures.length;
    
    // THE CRITICAL FIX: Ensure liveMetrics and liveMetrics.current exist before processing
    const currentMetrics = liveMetrics && liveMetrics.current ? Object.values(liveMetrics.current) : [];
    const avgCpu = currentMetrics.length > 0
        ? currentMetrics.reduce((acc, curr) => acc + (curr?.cpu || 0), 0) / currentMetrics.length
        : 0;

    const stats = [
        { label: "System-Status", value: "Operational", color: "text-noc-green", icon: <CheckCircle /> },
        { label: "Aktive Incidents", value: incidents.length, color: "text-noc-red", icon: <ShieldAlert /> },
        { label: "Sicherheits-Events", value: securityEvents.length, color: "text-noc-yellow", icon: <AlertCircle /> },
        { label: "Online-Geräte", value: `${onlineDevices} / ${totalDevices}`, color: "text-noc-blue", icon: <Server /> },
        { label: "Ø CPU-Last", value: `${avgCpu.toFixed(1)}%`, color: "text-noc-purple", icon: <Cpu /> },
    ];

    return (
        <div className="p-4 sm:p-6 lg:p-8">
            <h1 className="text-3xl font-bold text-noc-text mb-6">NOC/SOC Dashboard</h1>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6">
                {stats.map(stat => <StatCard key={stat.label} {...stat} />)}
            </div>
            <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-noc-light-dark p-4 rounded-lg border border-noc-border">
                    <h2 className="text-xl font-bold text-noc-text mb-4 px-2">Letzte Sicherheits-Events</h2>
                    <ul className="text-sm text-noc-text-secondary space-y-2 font-mono h-64 overflow-y-auto">
                        {securityEvents.length > 0 ? securityEvents.slice(0, 10).map(event => (
                            <li key={event.id} className="p-2 rounded-md hover:bg-noc-dark">
                                <span className="text-noc-yellow">[{new Date(event.timestamp).toLocaleTimeString()}]</span> {event.description}
                            </li>
                        )) : <li className="p-2">Keine Events.</li>}
                    </ul>
                </div>
                 <div className="bg-noc-light-dark p-4 rounded-lg border border-noc-border">
                    <h2 className="text-xl font-bold text-noc-text mb-4 px-2">Neue Incidents</h2>
                     <ul className="text-sm text-noc-text-secondary space-y-2 h-64 overflow-y-auto">
                        {incidents.length > 0 ? incidents.slice(0, 5).map((incident, index) => (
                            <li key={incident.id || index} className="p-3 rounded-md hover:bg-noc-dark border-l-2 border-noc-red">
                                <h3 className="font-bold text-noc-red">{incident.name}</h3>
                                <p className="text-xs mt-1">{incident.summary}</p>
                            </li>
                        )) : <li className="p-2">Keine neuen Incidents.</li>}
                    </ul>
                </div>
                <ScenarioControl />
                <SecurityControl />
            </div>
        </div>
    );
};

export default DashboardPage;