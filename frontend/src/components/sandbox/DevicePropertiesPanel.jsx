import React, { useState, useEffect, useContext } from 'react';
import { TopologyContext } from '../../contexts/TopologyContext';
import { X } from 'lucide-react';

const DevicePropertiesPanel = ({ device, onClose }) => {
    const { setTopology } = useContext(TopologyContext);
    const [properties, setProperties] = useState(device.properties);
    const [geometry, setGeometry] = useState(device.geometry);

    useEffect(() => {
        setProperties(device.properties);
        setGeometry(device.geometry);
    }, [device]);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        if (name.startsWith('details.')) {
            const detailKey = name.split('.')[1];
            setProperties(prev => ({
                ...prev,
                details: {
                    ...prev.details,
                    [detailKey]: value
                }
            }));
        } else {
            setProperties(prev => ({
                ...prev,
                [name]: type === 'checkbox' ? checked : value
            }));
        }
    };

    const handleSave = () => {
        setTopology(prev => ({
            ...prev,
            features: prev.features.map(f => 
                f.properties.id === device.properties.id 
                ? { ...f, properties: properties, geometry: geometry } 
                : f
            )
        }));
        onClose(); // Schließt das Panel nach dem Speichern
    };

    const renderPropertyInput = (key, value, path = '') => {
        const name = path ? `${path}.${key}` : key;
        if (typeof value === 'boolean') {
            return (
                <input 
                    type="checkbox" 
                    name={name} 
                    checked={value} 
                    onChange={handleChange} 
                    className="ml-2"
                />
            );
        }
        if (typeof value === 'number') {
            return (
                <input 
                    type="number" 
                    name={name} 
                    value={value} 
                    onChange={handleChange} 
                    className="w-full p-1 bg-noc-dark border border-noc-border rounded-md text-noc-text text-sm"
                    step="any"
                />
            );
        }
        if (typeof value === 'string' && (key.includes('ip_address') || key.includes('firmware'))) {
             return (
                <input 
                    type="text" 
                    name={name} 
                    value={value} 
                    onChange={handleChange} 
                    className="w-full p-1 bg-noc-dark border border-noc-border rounded-md text-noc-text text-sm"
                />
            );
        }
        // Für komplexe Objekte rekursiv rendern
        if (typeof value === 'object' && value !== null) {
            if (Array.isArray(value)) {
                return (
                    <div className="pl-2 border-l border-noc-border ml-2">
                        {value.map((item, idx) => (
                            <div key={idx} className="mt-1">
                                <span className="text-noc-text-secondary">{idx}: </span>
                                {renderPropertyInput(idx, item, `${name}`)}
                            </div>
                        ))}
                    </div>
                );
            }
            return (
                <div className="pl-2 border-l border-noc-border ml-2">
                    {Object.entries(value).map(([subKey, subValue]) => (
                        <div key={subKey} className="mt-1">
                            <span className="text-noc-text-secondary">{subKey}: </span>
                            {renderPropertyInput(subKey, subValue, `${name}`)}
                        </div>
                    ))}
                </div>
            );
        }
        return (
            <input 
                type="text" 
                name={name} 
                value={value} 
                onChange={handleChange} 
                className="w-full p-1 bg-noc-dark border border-noc-border rounded-md text-noc-text text-sm"
            />
        );
    };

    return (
        <div className="bg-noc-light-dark text-noc-text rounded-lg border border-noc-border p-4 h-full flex flex-col">
            <div className="flex justify-between items-center border-b border-noc-border pb-3 mb-3">
                <h3 className="text-lg font-bold">Eigenschaften von {properties.label}</h3>
                <button onClick={onClose} className="text-noc-text-secondary hover:text-white p-1 rounded-full hover:bg-noc-border">
                    <X size={16} />
                </button>
            </div>

            <div className="flex-grow overflow-y-auto space-y-2 text-sm">
                {Object.entries(properties).map(([key, value]) => (
                    <div key={key} className="flex items-center">
                        <label className="w-1/3 text-noc-text-secondary pr-2 truncate">{key}:</label>
                        <div className="w-2/3">
                            {renderPropertyInput(key, value)}
                        </div>
                    </div>
                ))}
            </div>

            <button 
                onClick={handleSave} 
                className="mt-4 py-2 px-4 bg-noc-blue text-white font-semibold rounded-md hover:bg-opacity-80"
            >
                Änderungen speichern
            </button>
        </div>
    );
};

export default DevicePropertiesPanel;