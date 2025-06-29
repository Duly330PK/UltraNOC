# frontend/Dockerfile

# --- Stufe 1: Builder ---
# Hier bauen wir die React-Anwendung
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
# Dieser Befehl kompiliert Ihr Frontend in den /app/dist Ordner
RUN npm run build

# --- Stufe 2: Finales Image ---
# Hier wird nur das Ergebnis des Builds und ein kleiner Server übernommen
FROM node:18-alpine
WORKDIR /app
# Installiere einen einfachen statischen Server
RUN npm install -g serve
# Kopiere nur die gebauten Dateien aus der Builder-Stufe
COPY --from=builder /app/dist ./public

# Expose Port und starte den Server, um den 'public' Ordner auszuliefern
EXPOSE 5173
CMD ["npx", "serve", "-s", "public", "-l", "5173"]