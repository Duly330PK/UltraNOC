import React, { useState, useContext, useEffect, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { TopologyContext } from '../../contexts/TopologyContext';
import { Search, X } from 'lucide-react';

const GlobalSearch = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [isFocused, setIsFocused] = useState(false);
    const { topology, focusOnElement } = useContext(TopologyContext);
    const navigate = useNavigate();
    const location = useLocation();
    const searchRef = useRef(null);

    useEffect(() => {
        if (query.length > 1) {
            const lowerCaseQuery = query.toLowerCase();
            const allFeatures = topology.features;

            const filtered = allFeatures.filter(feature => {
                const props = feature.properties;
                if (!props) return false;

                // Check top-level properties
                if (props.id?.toLowerCase().includes(lowerCaseQuery)) return true;
                if (props.label?.toLowerCase().includes(lowerCaseQuery)) return true;
                if (props.type?.toLowerCase().includes(lowerCaseQuery)) return true;
                if (props.status?.toLowerCase().includes(lowerCaseQuery)) return true;

                // Check details
                const details = props.details;
                if (details) {
                    if (details.ip_address?.toLowerCase().includes(lowerCaseQuery)) return true;
                    if (details.ipv6_address?.toLowerCase().includes(lowerCaseQuery)) return true;
                    if (details.manufacturer?.toLowerCase().includes(lowerCaseQuery)) return true;
                    if (details.model?.toLowerCase().includes(lowerCaseQuery)) return true;
                    if (details.customer_id?.toLowerCase().includes(lowerCaseQuery)) return true;
                }
                return false;
            });
            setResults(filtered);
        } else {
            setResults([]);
        }
    }, [query, topology]);
    
    // Close dropdown when clicking outside
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (searchRef.current && !searchRef.current.contains(event.target)) {
                setIsFocused(false);
            }
        };
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, [searchRef]);


    const handleSelect = (element) => {
        setQuery('');
        setResults([]);
        setIsFocused(false);

        // Fly to element on the map
        focusOnElement(element);

        // If not on a topology page, navigate there
        if (!location.pathname.includes('topology')) {
            navigate('/topology');
        }
    };

    return (
        <div className="relative w-full max-w-md" ref={searchRef}>
            <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-noc-text-secondary" size={20} />
                <input
                    type="text"
                    placeholder="Suche Geräte, IP, Standort, Kunde..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onFocus={() => setIsFocused(true)}
                    className="w-full bg-noc-light-dark border border-noc-border rounded-lg py-2 pl-10 pr-4 text-noc-text focus:outline-none focus:ring-2 focus:ring-noc-blue"
                />
                {query && (
                    <button onClick={() => setQuery('')} className="absolute right-3 top-1/2 -translate-y-1/2 text-noc-text-secondary hover:text-white">
                        <X size={16}/>
                    </button>
                )}
            </div>

            {isFocused && results.length > 0 && (
                <div className="absolute z-10 mt-2 w-full bg-noc-light-dark border border-noc-border rounded-lg shadow-lg max-h-96 overflow-y-auto">
                    <ul>
                        {results.map((item, index) => (
                            <li
                                key={item.properties.id || index}
                                onClick={() => handleSelect(item)}
                                className="px-4 py-3 hover:bg-noc-blue cursor-pointer border-b border-noc-border last:border-b-0"
                            >
                                <p className="font-bold text-noc-text">{item.properties.label || item.properties.id}</p>
                                <p className="text-sm text-noc-text-secondary">{item.properties.type}</p>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default GlobalSearch;