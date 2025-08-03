from fastapi import APIRouter
from app.api.v1.endpoints import users, curriculum, progress, agent

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(curriculum.router, prefix="/curriculum", tags=["curriculum"])
api_router.include_router(progress.router, prefix="/progress", tags=["progress"])
api_router.include_router(agent.router, prefix="/agent", tags=["agent"]) 