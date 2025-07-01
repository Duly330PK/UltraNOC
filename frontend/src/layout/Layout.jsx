import React, { useContext } from 'react';
import { Outlet, NavLink } from 'react-router-dom';
import { AuthContext } from '../contexts/AuthContext';
import { CommandMenuContext } from '../contexts/CommandMenuContext';
import { ThemeContext } from '../contexts/ThemeContext';
import { BarChart2, Compass, Globe, Shield, Search, LogOut, TerminalSquare, Box, HardDrive, Moon, Sun } from 'lucide-react';
import GlobalSearch from '../components/shared/GlobalSearch'; // Import the new component

const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: <BarChart2 size={18} /> },
    { path: '/topology', label: '2D-Topologie', icon: <Compass size={18} /> },
    { path: '/topology-3d', label: '3D-Topologie', icon: <Globe size={18} /> },
    { path: '/incidents', label: 'Incidents', icon: <Shield size={18} /> },
    { path: '/forensics', label: 'Forensik', icon: <Search size={18} /> },
    { path: '/devices', label: 'Geräteübersicht', icon: <HardDrive size={18} /> },
    { path: '/sandbox', label: 'Sandbox Editor', icon: <Box size={18} /> },
];

const Layout = () => {
    const { logout } = useContext(AuthContext);
    const { toggleCommandMenu } = useContext(CommandMenuContext);
    const { theme, toggleTheme } = useContext(ThemeContext);

    return (
        <div className="flex h-screen bg-lm-bg text-lm-text dark:bg-noc-dark dark:text-noc-text">
            {/* Sidebar */}
            <aside className="w-64 bg-lm-bg-secondary dark:bg-noc-light-dark flex-shrink-0 flex flex-col border-r border-lm-border dark:border-noc-border">
                <div className="h-16 flex items-center justify-center text-xl font-bold border-b border-lm-border dark:border-noc-border">
                    <img src="/logo.svg" alt="UltraNOC Logo" className="h-8 w-8 mr-2" />
                    UltraNOC
                </div>
                <nav className="flex-1 px-2 py-4 space-y-1">
                    {navItems.map((item) => (
                        <NavLink
                            key={item.path}
                            to={item.path}
                            className={({ isActive }) =>
                                `flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium
                                 text-lm-text-secondary dark:text-noc-text-secondary
                                 hover:bg-lm-border dark:hover:bg-noc-border 
                                 hover:text-lm-text dark:hover:text-noc-text 
                                 transition-colors duration-200 
                                 ${isActive ? 'bg-noc-blue text-white' : ''}`
                            }
                        >
                            {item.icon}
                            <span>{item.label}</span>
                        </NavLink>
                    ))}
                </nav>
                <div className="px-2 py-4 border-t border-lm-border dark:border-noc-border space-y-2">
                    <button
                        onClick={toggleTheme}
                        className="w-full flex items-center gap-3 px-3 py-2 text-lm-text-secondary dark:text-noc-text-secondary rounded-md text-sm font-medium hover:bg-lm-border dark:hover:bg-noc-border transition-colors duration-200"
                    >
                        {theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
                        <span>{theme === 'dark' ? 'Heller Modus' : 'Dunkler Modus'}</span>
                    </button>
                    <button
                        onClick={toggleCommandMenu}
                        className="w-full flex items-center gap-3 px-3 py-2 text-lm-text-secondary dark:text-noc-text-secondary rounded-md text-sm font-medium hover:bg-lm-border dark:hover:bg-noc-border transition-colors duration-200"
                    >
                        <TerminalSquare size={18} />
                        <span>Befehlsmenü</span>
                        <kbd className="ml-auto text-xs border border-lm-border dark:border-noc-border rounded px-1.5 py-0.5">Ctrl+K</kbd>
                    </button>
                    <button
                        onClick={logout}
                        className="w-full flex items-center gap-3 px-3 py-2 text-lm-text-secondary dark:text-noc-text-secondary rounded-md text-sm font-medium hover:bg-noc-red hover:text-white transition-colors duration-200"
                    >
                        <LogOut size={18} />
                        <span>Logout</span>
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <div className="flex-1 flex flex-col overflow-hidden">
                {/* NEW: Main Header with Global Search */}
                <header className="flex-shrink-0 bg-lm-bg-secondary dark:bg-noc-light-dark border-b border-lm-border dark:border-noc-border h-16 flex items-center px-6">
                    <GlobalSearch />
                </header>
                <main className="flex-1 overflow-x-hidden overflow-y-auto bg-lm-bg dark:bg-noc-dark">
                    <Outlet />
                </main>
            </div>
        </div>
    );
};

export default Layout;