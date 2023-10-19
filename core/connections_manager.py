from typing import Dict

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: int) -> None:
        await websocket.accept()
        self.active_connections.update({client_id: websocket})

    async def disconnect(self, client_id: int) -> WebSocket | None:
        try:
            self.active_connections.pop(client_id)
        except KeyError:
            pass

    async def get_receiver(self, receiver_id: int) -> WebSocket | None:
        return self.active_connections.get(receiver_id)
