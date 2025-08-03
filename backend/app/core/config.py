from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/curriculum_architect"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # AI/LLM - Support both OpenAI and Google Gemini
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    AI_PROVIDER: str = "openai"  # "openai" or "gemini"
    
    # Vector Database
    WEAVIATE_URL: str = "http://localhost:8080"
    
    # Email Service
    SENDGRID_API_KEY: str = ""
    FROM_EMAIL: str = "noreply@curriculumarchitect.com"
    
    # Firebase (Push Notifications)
    FIREBASE_CREDENTIALS: str = ""
    
    # Redis (for background tasks)
    REDIS_URL: str = "redis://localhost:6379"
    
    # Background Tasks
    ENABLE_BACKGROUND_TASKS: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 