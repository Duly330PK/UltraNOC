import React, { createContext, useState } from 'react';

export const SandboxContext = createContext();

export const SandboxProvider = ({ children }) => {
    const [sandboxMode, setSandboxMode] = useState('view'); // 'view', 'addNode', 'addLinkStart', 'addLinkEnd'
    const [nodeTypeToAdd, setNodeTypeToAdd] = useState('Core Router');
    const [linkSourceNode, setLinkSourceNode] = useState(null);

    const value = {
        sandboxMode,
        setSandboxMode,
        nodeTypeToAdd,
        setNodeTypeToAdd,
        linkSourceNode,
        setLinkSourceNode
    };

    return (
        <SandboxContext.Provider value={value}>
            {children}
        </SandboxContext.Provider>
    );
};