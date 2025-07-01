import React, { useState, useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import { Navigate } from 'react-router-dom';

const LoginPage = () => {
    const [username, setUsername] = useState('admin');
    const [password, setPassword] = useState('admin123');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const { login, isAuthenticated } = useContext(AuthContext);

    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);
        try {
            await login(username, password);
        } catch (err) {
            setError(err.message || 'Login fehlgeschlagen. Bitte überprüfen Sie Ihre Zugangsdaten.');
        } finally {
            setIsLoading(false);
        }
    };

    if (isAuthenticated) {
        return <Navigate to="/dashboard" />;
    }

    return (
        <div className="login-container">
            <div className="w-full max-w-sm p-8 space-y-8 bg-noc-light-dark/80 backdrop-blur-sm rounded-lg shadow-2xl border border-noc-border">
                <div className="text-center">
                    <img src="/logo.svg" alt="UltraNOC Logo" className="w-16 h-16 mx-auto mb-4" />
                    <h1 className="text-2xl font-bold text-noc-text">UltraNOC Login</h1>
                    <p className="text-noc-text-secondary">Unified Operations Platform</p>
                </div>
                <form className="space-y-6" onSubmit={handleLogin}>
                    <div>
                        <label htmlFor="username" className="sr-only">Username</label>
                        <input
                            id="username"
                            name="username"
                            type="text"
                            autoComplete="username"
                            required
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="w-full px-3 py-2 bg-noc-dark border border-noc-border rounded-md text-noc-text placeholder-noc-text-secondary focus:outline-none focus:ring-2 focus:ring-noc-blue"
                            placeholder="Username"
                        />
                    </div>
                    <div>
                        <label htmlFor="password" className="sr-only">Password</label>
                        <input
                            id="password"
                            name="password"
                            type="password"
                            autoComplete="current-password"
                            required
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full px-3 py-2 bg-noc-dark border border-noc-border rounded-md text-noc-text placeholder-noc-text-secondary focus:outline-none focus:ring-2 focus:ring-noc-blue"
                            placeholder="Password"
                        />
                    </div>
                    {error && <p className="text-sm text-noc-red text-center">{error}</p>}
                    <div>
                        <button
                            type="submit"
                            disabled={isLoading}
                            className="w-full py-2 px-4 bg-noc-blue text-white font-semibold rounded-md hover:bg-opacity-80 transition-all disabled:bg-noc-border disabled:cursor-not-allowed"
                        >
                            {isLoading ? 'Signing In...' : 'Sign In'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default LoginPage;