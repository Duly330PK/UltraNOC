import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App.jsx';
import './index.css';
import { AuthProvider } from './contexts/AuthContext.jsx';
import { CommandMenuProvider } from './contexts/CommandMenuContext.jsx';
import { ThemeProvider } from './contexts/ThemeContext.jsx';

// FIX: Only wrap with providers that DON'T make API calls on load.
// TopologyProvider and SandboxProvider are moved into App.jsx
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <ThemeProvider>
        <CommandMenuProvider>
          <AuthProvider>
            <App />
          </AuthProvider>
        </CommandMenuProvider>
      </ThemeProvider>
    </BrowserRouter>
  </React.StrictMode>
);