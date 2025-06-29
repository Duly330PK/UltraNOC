import React, { createContext, useState } from 'react';

export const CommandMenuContext = createContext();

export const CommandMenuProvider = ({ children }) => {
    const [isOpen, setOpen] = useState(false);

    const toggleCommandMenu = () => {
        setOpen(prev => !prev);
    };

    return (
        <CommandMenuContext.Provider value={{ isOpen, setOpen, toggleCommandMenu }}>
            {children}
        </CommandMenuContext.Provider>
    );
};