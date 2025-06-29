import React, { createContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUser } from '../api/auth';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(localStorage.getItem('ultranoc_token'));
    const navigate = useNavigate();

    const login = async (username, password) => {
        const data = await loginUser(username, password);
        localStorage.setItem('ultranoc_token', data.access_token);
        setToken(data.access_token);
        navigate('/dashboard');
    };

    const logout = () => {
        localStorage.removeItem('ultranoc_token');
        setToken(null);
        navigate('/login', { replace: true });
    };

    const authContextValue = {
        token,
        login,
        logout,
        isAuthenticated: !!token,
    };

    return (
        <AuthContext.Provider value={authContextValue}>
            {children}
        </AuthContext.Provider>
    );
};