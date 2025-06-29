import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true, // Wichtig für Docker
    proxy: {
      '/api': {
        target: 'http://backend:8000', // Docker-interner Service-Name
        changeOrigin: true,
      },
       '/ws': {
        target: 'ws://backend:8000', // WebSocket-Proxy
        ws: true,
      },
    }
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    }
  }
});