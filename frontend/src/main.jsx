import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App.jsx';
import './index.css';
import { AuthProvider } from './contexts/AuthContext.jsx';
import { TopologyProvider } from './contexts/TopologyContext.jsx';
import { CommandMenuProvider } from './contexts/CommandMenuContext.jsx';
import { ThemeProvider } from './contexts/ThemeContext.jsx';
import { SandboxProvider } from './contexts/SandboxContext.jsx';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <ThemeProvider>
        <AuthProvider>
          <TopologyProvider>
            <SandboxProvider>
              <CommandMenuProvider>
                <App />
              </CommandMenuProvider>
            </SandboxProvider>
          </TopologyProvider>
        </AuthProvider>
      </ThemeProvider>
    </BrowserRouter>
  </React.StrictMode>
);
