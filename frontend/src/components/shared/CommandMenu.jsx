import React, { useContext, useEffect } from 'react';
import { Command } from 'cmdk';
import { CommandMenuContext } from '../../contexts/CommandMenuContext';
import { useNavigate } from 'react-router-dom';
import { BarChart2, Compass, Shield, Search, LogOut, Globe } from 'lucide-react';

export default function CommandMenu() {
    const { isOpen, setOpen } = useContext(CommandMenuContext);
    const navigate = useNavigate();

    // Schließt das Menü bei einem Routenwechsel
    useEffect(() => {
        if (isOpen) {
            const handleRouteChange = () => setOpen(false);
            // Ein einfacher Weg, um auf Navigation zu hören.
            // In komplexeren Apps könnte dies über den Router-Kontext erfolgen.
            window.addEventListener('popstate', handleRouteChange);
            return () => window.removeEventListener('popstate', handleRouteChange);
        }
    }, [isOpen, setOpen, navigate]);

    const runCommand = (command) => {
        setOpen(false);
        command();
    };

    const commandItems = [
        { 
            heading: "Navigation", 
            items: [
                { label: "Dashboard", action: () => navigate('/dashboard'), icon: <BarChart2 size={16}/> },
                { label: "Topologie (2D)", action: () => navigate('/topology'), icon: <Compass size={16}/> },
                { label: "Topologie (3D)", action: () => navigate('/topology-3d'), icon: <Globe size={16}/> },
                { label: "Incidents", action: () => navigate('/incidents'), icon: <Shield size={16}/> },
                { label: "Forensik", action: () => navigate('/forensics'), icon: <Search size={16}/> },
            ]
        },
        { 
            heading: "Aktionen", 
            items: [
                { 
                    label: "Logout", 
                    // Wir verwenden ein Custom Event, um die Logout-Funktion aus dem AuthContext aufzurufen,
                    // da wir hier keinen direkten Zugriff darauf haben.
                    action: () => window.dispatchEvent(new CustomEvent('logout-request')), 
                    icon: <LogOut size={16}/> 
                }
            ]
        }
    ];

    if (!isOpen) return null;

    return (
        <Command.Dialog open={isOpen} onOpenChange={setOpen} label="Global Command Menu">
             <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50" onClick={() => setOpen(false)} />
             <div className="fixed top-[20vh] left-1/2 -translate-x-1/2 w-full max-w-xl z-50">
                <div className="bg-noc-light-dark text-noc-text border border-noc-border rounded-lg shadow-lg">
                    <Command.Input 
                        placeholder="Befehl oder Seite suchen..."
                        className="w-full text-lg bg-transparent p-4 border-b border-noc-border outline-none" 
                    />
                    <Command.List className="p-2 max-h-[400px] overflow-y-auto">
                        <Command.Empty>Keine Ergebnisse gefunden.</Command.Empty>
                        {commandItems.map((group) => (
                           <Command.Group key={group.heading} heading={group.heading} className="text-xs text-noc-text-secondary px-2 py-1 uppercase tracking-wider">
                                {group.items.map(item => (
                                    <Command.Item 
                                        key={item.label}
                                        onSelect={item.action ? () => runCommand(item.action) : undefined}
                                        className="flex items-center gap-3 p-3 rounded-md hover:bg-noc-border cursor-pointer aria-selected:bg-noc-blue aria-selected:text-white"
                                    >
                                        {item.icon}
                                        <span className="text-base text-noc-text">{item.label}</span>
                                    </Command.Item>
                                ))}
                           </Command.Group>
                        ))}
                    </Command.List>
                </div>
            </div>
        </Command.Dialog>
    );
}