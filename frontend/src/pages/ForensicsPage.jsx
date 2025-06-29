import React, { useState, useContext } from 'react';
import { TopologyContext } from '../contexts/TopologyContext';
import { useNavigate } from 'react-router-dom';
import { Search, Clock, Hash } from 'lucide-react';

const ForensicsPage = () => {
  const [ipAddress, setIpAddress] = useState('91.194.84.73');
  const [port, setPort] = useState('40965');
  const [timestamp, setTimestamp] = useState(new Date().toISOString().slice(0, 16));
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const { traceAndShowOnMap } = useContext(TopologyContext);
  const navigate = useNavigate();

  const handleTrace = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setResult(null);

    const token = localStorage.getItem('ultranoc_token');
    try {
      const response = await fetch('/api/v1/forensics/trace', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify({
          ip_address: ipAddress,
          port: parseInt(port),
          timestamp: new Date(timestamp).toISOString(),
        }),
      });

      if (!response.ok) {
          const errData = await response.json();
          throw new Error(errData.detail || 'Suche fehlgeschlagen.');
      }
      const data = await response.json();
      setResult(data);

    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const showOnMap = () => {
    if (result && result.found && result.device_id) {
        traceAndShowOnMap(result.device_id);
        navigate('/topology');
    }
  };

  return (
    <div className="p-4 sm:p-6 lg:p-8 h-full flex flex-col text-noc-text">
       <h1 className="text-2xl font-bold mb-4">Forensische Verbindungsanalyse</h1>
       <p className="text-noc-text-secondary mb-6">Verfolgen Sie eine öffentliche IP-Adresse und einen Port zu einem bestimmten Zeitpunkt zurück, um den zugehörigen Kundenanschluss zu identifizieren.</p>

       <form onSubmit={handleTrace} className="bg-noc-light-dark p-6 rounded-lg border border-noc-border max-w-2xl">
           <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
             <div>
               <label htmlFor="ipAddress" className="block text-sm font-medium text-noc-text-secondary mb-1">Öffentliche IP-Adresse</label>
               <input type="text" id="ipAddress" value={ipAddress} onChange={(e) => setIpAddress(e.target.value)} className="w-full bg-noc-dark border border-noc-border rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-noc-blue" required />
             </div>
             <div>
               <label htmlFor="port" className="block text-sm font-medium text-noc-text-secondary mb-1">Port</label>
               <input type="number" id="port" value={port} onChange={(e) => setPort(e.target.value)} className="w-full bg-noc-dark border border-noc-border rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-noc-blue" required />
             </div>
             <div>
               <label htmlFor="timestamp" className="block text-sm font-medium text-noc-text-secondary mb-1">Zeitstempel (UTC)</label>
               <input type="datetime-local" id="timestamp" value={timestamp} onChange={(e) => setTimestamp(e.target.value)} className="w-full bg-noc-dark border border-noc-border rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-noc-blue" required />
             </div>
           </div>
           <div className="mt-6">
             <button type="submit" disabled={isLoading} className="w-full flex items-center justify-center gap-2 bg-noc-blue text-white py-2 px-4 rounded-md hover:bg-opacity-80 disabled:bg-noc-border disabled:cursor-not-allowed">
               <Search size={16} />
               {isLoading ? 'Suche läuft...' : 'Verbindung verfolgen'}
             </button>
           </div>
       </form>

       {error && <div className="mt-6 p-4 bg-noc-red bg-opacity-20 text-noc-red rounded-md max-w-2xl">{error}</div>}

       {result && (
            <div className="mt-6 bg-noc-light-dark p-6 rounded-lg border border-noc-border max-w-2xl">
                <h2 className="text-xl font-bold mb-4">Analyseergebnis</h2>
                {result.found ? (
                    <div>
                        <p className="text-noc-green font-bold mb-4">Kundenanschluss erfolgreich identifiziert!</p>
                        <div className="grid grid-cols-2 gap-4 font-mono text-sm">
                            <div className="text-noc-text-secondary">Kunden-ID:</div><div className="text-noc-text">{result.customer_id}</div>
                            <div className="text-noc-text-secondary">Interne IP:</div><div className="text-noc-text">{result.internal_ip}</div>
                            <div className="text-noc-text-secondary">Segment:</div><div className="text-noc-text">{result.segment}</div>
                            <div className="text-noc-text-secondary">Gerät (ONT):</div><div className="text-noc-text">{result.device_id}</div>
                        </div>
                        <button onClick={showOnMap} className="mt-6 bg-noc-green text-white py-2 px-4 rounded-md hover:bg-opacity-80">Auf Karte anzeigen</button>
                    </div>
                ) : (
                    <p className="text-noc-yellow">Für die angegebenen Daten konnte kein passender Log-Eintrag gefunden werden.</p>
                )}
            </div>
       )}
    </div>
  );
};

export default ForensicsPage;