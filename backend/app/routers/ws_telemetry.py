from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio

router = APIRouter()

clients = []

@router.websocket("/ws/telemetry")
async def telemetry_ws(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await websocket.send_json({"msg": "heartbeat"})
            await asyncio.sleep(3)
    except WebSocketDisconnect:
        clients.remove(websocket)
