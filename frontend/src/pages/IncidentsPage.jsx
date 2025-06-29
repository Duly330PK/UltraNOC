import React, { useContext, useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { TopologyContext } from '../contexts/TopologyContext';
import SocPanel from '../components/incidents/SocPanel';
import IncidentGraph from '../components/incidents/IncidentGraph';
import { ShieldAlert } from 'lucide-react';

const IncidentsPage = () => {
    // Echte Incident-Daten aus dem Context holen
    const { incidents } = useContext(TopologyContext);
    // Lokalen State für den ausgewählten Incident hinzufügen
    const [selectedIncident, setSelectedIncident] = useState(null);
    const { id } = useParams(); // Falls eine ID über die URL kommt

    // Effekt, um den ausgewählten Incident zu setzen, wenn sich die Liste ändert
    // oder eine ID in der URL vorhanden ist.
    useEffect(() => {
        if (id && incidents.length > 0) {
            const incidentFromUrl = incidents.find(inc => inc.id === parseInt(id));
            setSelectedIncident(incidentFromUrl);
        } else if (!selectedIncident && incidents.length > 0) {
            // Automatisch den neuesten Incident auswählen, wenn noch keiner gewählt ist
            setSelectedIncident(incidents[0]);
        }
    }, [id, incidents, selectedIncident]);


    return (
        <div className="flex h-full w-full p-4 gap-4 text-noc-text">
            {/* Linke Spalte: Liste der Incidents */}
            <div className="w-1/3 bg-noc-light-dark rounded-lg border border-noc-border p-4 flex flex-col">
                <h2 className="text-xl font-bold mb-4">Aktive Incidents</h2>
                <ul className="flex-grow overflow-y-auto space-y-2">
                    {incidents.length > 0 ? (
                        incidents.map((incident, index) => (
                            <li
                                key={index}
                                onClick={() => setSelectedIncident(incident)}
                                className={`p-3 rounded-md cursor-pointer border-l-4 transition-colors
                                    ${selectedIncident === incident
                                        ? 'bg-noc-blue/20 border-noc-blue'
                                        : 'bg-noc-dark border-noc-red hover:bg-noc-border'
                                    }`}
                            >
                                <h3 className="font-bold text-noc-text">{incident.name}</h3>
                                <p className="text-xs text-noc-text-secondary mt-1 truncate">{incident.summary}</p>
                            </li>
                        ))
                    ) : (
                        <li className="text-center text-noc-text-secondary pt-10">
                            <ShieldAlert className="mx-auto h-12 w-12" />
                            <p className="mt-2">Keine aktiven Incidents.</p>
                        </li>
                    )}
                </ul>
            </div>

            {/* Rechte Spalte: Details des ausgewählten Incidents */}
            <div className="w-2/3 flex flex-col gap-4">
                {selectedIncident ? (
                    <>
                        <div className="h-2/3">
                            <IncidentGraph incident={selectedIncident} />
                        </div>
                        <div className="h-1/3">
                            <SocPanel incident={selectedIncident} />
                        </div>
                    </>
                ) : (
                     <div className="w-full h-full bg-noc-light-dark rounded-lg border border-noc-border flex items-center justify-center">
                        <p className="text-noc-text-secondary">Bitte wählen Sie einen Vorfall aus der Liste aus.</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default IncidentsPage;