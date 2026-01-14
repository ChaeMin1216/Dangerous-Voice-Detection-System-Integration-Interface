# app/websocket_manager.py

#from fastapi import WebSocket
#from typing import List

# class WebSocketManager:
#    def __init__(self):
#        self.active_connections: List[WebSocket] = []
    
#    async def connect(self, websocket: WebSocket):
#        await websocket.accept()
#        self.active_connections.append(websocket)
    
#    def disconnect(self, websocket: WebSocket):
#        self.active_connections.remove(websocket)
    
#    async def send_json(self, message: dict):
#        for connection in self.active_connections:
#            await connection.send_json(message)

# 웹소켓 매니저 인스턴스 생성
#websocket_manager = WebSocketManager()

from fastapi import WebSocket, WebSocketDisconnect
from typing import List

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_json(self, message: dict):
        disconnected_connections = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                disconnected_connections.append(connection)
            except Exception as e:
                print(f"Error sending message: {e}")
                disconnected_connections.append(connection)

        # Clean up disconnected connections
        for connection in disconnected_connections:
            self.disconnect(connection)

# 웹소켓 매니저 인스턴스 생성
websocket_manager = WebSocketManager()

