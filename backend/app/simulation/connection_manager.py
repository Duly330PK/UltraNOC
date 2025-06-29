from fastapi import WebSocket
from typing import List
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        # Erstelle eine Kopie, um Thread-Safety-Probleme bei Verbindungsabbrüchen zu vermeiden
        # während der Iteration.
        connections = self.active_connections[:]
        for connection in connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception:
                # Verbindung könnte bereits geschlossen sein, entferne sie sicher
                self.disconnect(connection)