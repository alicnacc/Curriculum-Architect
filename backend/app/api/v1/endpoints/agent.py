from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user
from app.services.agent_service import AgentService
from pydantic import BaseModel
from typing import Dict, Any
import json

router = APIRouter()

class ChatMessage(BaseModel):
    message: str
    curriculum_id: int = None

@router.post("/chat")
async def chat_with_agent(
    chat_data: ChatMessage,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Chat with the AI agent"""
    try:
        agent_service = AgentService()
        response = await agent_service.chat(
            user_id=current_user["user_id"],
            message=chat_data.message,
            curriculum_id=chat_data.curriculum_id,
            db=db
        )
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get agent response: {str(e)}"
        )

# WebSocket endpoint for real-time chat
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket)
    agent_service = AgentService()
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Process message with agent
            response = await agent_service.chat(
                user_id=user_id,
                message=message_data.get("message", ""),
                curriculum_id=message_data.get("curriculum_id"),
                db=None  # WebSocket doesn't have db session
            )
            
            # Send response back
            await manager.send_personal_message(
                json.dumps({"response": response}),
                websocket
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket) 