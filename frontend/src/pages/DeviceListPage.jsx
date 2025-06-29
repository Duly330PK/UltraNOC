// frontend/src/pages/DeviceListPage.jsx

import React, { useState, useEffect, useCallback } from 'react';
import { HardDrive, ChevronLeft, ChevronRight, Search } from 'lucide-react';

const StatusIndicator = ({ status }) => {
    const colorMap = {
        online: 'bg-noc-green',
        offline: 'bg-noc-red',
        rebooting: 'bg-noc-yellow',
        maintenance: 'bg-noc-purple',
        critical: 'bg-noc-red',
        warning: 'bg-noc-yellow',
        default: 'bg-noc-text-secondary'
    };
    const color = colorMap[status] || colorMap.default;
    return (
        <div className="flex items-center gap-2">
            <span className={`h-2.5 w-2.5 rounded-full ${color}`}></span>
            <span className="capitalize">{status}</span>
        </div>
    );
};

const DeviceListPage = () => {
    const [devices, setDevices] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(0);
    const [searchTerm, setSearchTerm] = useState('');
    const [debouncedSearchTerm, setDebouncedSearchTerm] = useState('');
    
    const DEVICES_PER_PAGE = 25;

    // Debounce-Effekt für die Sucheingabe
    useEffect(() => {
        const handler = setTimeout(() => {
            setDebouncedSearchTerm(searchTerm);
            setPage(1); // Bei neuer Suche auf Seite 1 zurücksetzen
        }, 500); // 500ms warten nach der letzten Eingabe

        return () => {
            clearTimeout(handler);
        };
    }, [searchTerm]);

    const fetchDevices = useCallback(async (currentPage, search) => {
        setLoading(true);
        setError(null);
        const token = localStorage.getItem('ultranoc_token');
        const skip = (currentPage - 1) * DEVICES_PER_PAGE;
        
        let url = `/api/v1/devices/?skip=${skip}&limit=${DEVICES_PER_PAGE}`;
        if (search) {
            url += `&search=${encodeURIComponent(search)}`;
        }

        try {
            const response = await fetch(url, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            setDevices(data.devices);
            setTotalPages(Math.ceil(data.total_count / DEVICES_PER_PAGE));
        } catch (e) {
            setError(e.message);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchDevices(page, debouncedSearchTerm);
    }, [page, debouncedSearchTerm, fetchDevices]);

    return (
        <div className="p-4 sm:p-6 lg:p-8 text-noc-text">
            <div className="flex items-center justify-between mb-6">
                <h1 className="text-3xl font-bold flex items-center gap-3">
                    <HardDrive size={32} />
                    Geräteübersicht
                </h1>
                <div className="relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-noc-text-secondary" size={20} />
                    <input 
                        type="text"
                        placeholder="Gerät suchen..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="bg-noc-light-dark border border-noc-border rounded-lg py-2 pl-10 pr-4 w-64 focus:outline-none focus:ring-2 focus:ring-noc-blue"
                    />
                </div>
            </div>
            
            <div className="bg-noc-light-dark border border-noc-border rounded-lg overflow-hidden">
                <table className="w-full text-left">
                    <thead className="bg-noc-dark text-sm text-noc-text-secondary uppercase">
                        <tr>
                            <th className="p-4">Status</th>
                            <th className="p-4">Label</th>
                            <th className="p-4">ID</th>
                            <th className="p-4">Typ</th>
                        </tr>
                    </thead>
                    <tbody>
                        {loading ? (
                            <tr><td colSpan="4" className="text-center p-8">Lade Geräte...</td></tr>
                        ) : error ? (
                            <tr><td colSpan="4" className="text-center p-8 text-noc-red">Fehler: {error}</td></tr>
                        ) : devices.length > 0 ? (
                            devices.map(device => (
                                <tr key={device.id} className="border-t border-noc-border hover:bg-noc-dark">
                                    <td className="p-4"><StatusIndicator status={device.status} /></td>
                                    <td className="p-4 font-semibold">{device.label}</td>
                                    <td className="p-4 font-mono text-sm text-noc-text-secondary">{device.id}</td>
                                    <td className="p-4">{device.type}</td>
                                </tr>
                            ))
                        ) : (
                             <tr><td colSpan="4" className="text-center p-8">Keine Geräte gefunden.</td></tr>
                        )}
                    </tbody>
                </table>
            </div>
            
            {/* Paginierung */}
            <div className="flex justify-center items-center gap-4 mt-6">
                <button 
                    onClick={() => setPage(p => Math.max(1, p - 1))}
                    disabled={page <= 1 || loading}
                    className="p-2 rounded-md bg-noc-border hover:bg-noc-blue disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    <ChevronLeft />
                </button>
                <span className="font-semibold">Seite {page} von {totalPages}</span>
                <button 
                    onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                    disabled={page >= totalPages || loading}
                    className="p-2 rounded-md bg-noc-border hover:bg-noc-blue disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    <ChevronRight />
                </button>
            </div>
        </div>
    );
};

export default DeviceListPage;