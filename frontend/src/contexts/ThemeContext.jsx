// frontend/src/contexts/ThemeContext.jsx

import React, { createContext, useState, useEffect } from 'react';

export const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
    // Standard-Theme aus dem localStorage lesen oder 'dark' verwenden
    const [theme, setTheme] = useState(localStorage.getItem('ultranoc_theme') || 'dark');

    useEffect(() => {
        const root = window.document.documentElement;
        
        // Entferne die alte Klasse und füge die neue hinzu
        const oldTheme = theme === 'dark' ? 'light' : 'dark';
        root.classList.remove(oldTheme);
        root.classList.add(theme);

        // Speichere die aktuelle Auswahl im localStorage
        localStorage.setItem('ultranoc_theme', theme);
    }, [theme]);

    const toggleTheme = () => {
        setTheme(prevTheme => prevTheme === 'dark' ? 'light' : 'dark');
    };

    return (
        <ThemeContext.Provider value={{ theme, toggleTheme }}>
            {children}
        </ThemeContext.Provider>
    );
};