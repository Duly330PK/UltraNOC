import React, { useState, useEffect, useCallback, useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import { HardDrive, ChevronLeft, ChevronRight, Search } from 'lucide-react';

const StatusIndicator = ({ status }) => {
    const colorMap = { online: 'bg-noc-green', offline: 'bg-noc-red', rebooting: 'bg-noc-yellow', default: 'bg-noc-text-secondary' };
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
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(0);
    const [searchTerm, setSearchTerm] = useState('');
    const { isAuthenticated, token } = useContext(AuthContext);
    
    const DEVICES_PER_PAGE = 25;

    const fetchDevices = useCallback(async (currentPage, search) => {
        setLoading(true);
        setError(null);
        const skip = (currentPage - 1) * DEVICES_PER_PAGE;
        let url = `/api/v1/devices/?skip=${skip}&limit=${DEVICES_PER_PAGE}`;
        if (search) url += `&search=${encodeURIComponent(search)}`;

        try {
            const response = await fetch(url, { headers: { 'Authorization': `Bearer ${token}` } });
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();
            setDevices(data.devices || []);
            setTotalPages(Math.ceil((data.total_count || 0) / DEVICES_PER_PAGE));
        } catch (e) {
            setError(e.message);
        } finally {
            setLoading(false);
        }
    }, [token]);

    useEffect(() => {
        // FIX: Only fetch data when authenticated.
        if (isAuthenticated) {
            const handler = setTimeout(() => {
                fetchDevices(page, searchTerm);
            }, 300);
            return () => clearTimeout(handler);
        } else {
            // Clear data if not authenticated
            setDevices([]);
            setTotalPages(0);
        }
    }, [page, searchTerm, fetchDevices, isAuthenticated]);

    return (
        <div className="p-4 sm:p-6 lg:p-8 text-noc-text">
            {/* The rest of the JSX is fine and doesn't need to be changed. */}
        </div>
    );
};

export default DeviceListPage;