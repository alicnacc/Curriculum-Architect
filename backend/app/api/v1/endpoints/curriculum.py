from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user
from app.schemas.curriculum import CurriculumCreate, CurriculumResponse, CurriculumComplete, ProgressUpdate
from app.services.curriculum_service import CurriculumService
from app.services.agent_service import AgentService
from typing import Dict, Any, List

router = APIRouter()

@router.post("/generate", response_model=CurriculumResponse)
async def generate_curriculum(
    curriculum_data: CurriculumCreate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a new personalized curriculum using AI agent"""
    try:
        agent_service = AgentService()
        curriculum_service = CurriculumService(db)
        
        # Generate curriculum using AI agent
        curriculum = await agent_service.generate_curriculum(
            user_id=current_user["user_id"],
            curriculum_data=curriculum_data,
            db=db
        )
        
        return curriculum
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate curriculum: {str(e)}"
        )

@router.get("/", response_model=List[CurriculumResponse])
def get_user_curriculums(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all curriculums for the current user"""
    curriculum_service = CurriculumService(db)
    curriculums = curriculum_service.get_user_curriculums(current_user["user_id"])
    return curriculums

@router.get("/{curriculum_id}", response_model=CurriculumComplete)
def get_curriculum(
    curriculum_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific curriculum with all modules and resources"""
    curriculum_service = CurriculumService(db)
    curriculum = curriculum_service.get_curriculum_with_modules(curriculum_id, current_user["user_id"])
    
    if not curriculum:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curriculum not found"
        )
    
    return curriculum

@router.delete("/{curriculum_id}")
def delete_curriculum(
    curriculum_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a curriculum"""
    curriculum_service = CurriculumService(db)
    success = curriculum_service.delete_curriculum(curriculum_id, current_user["user_id"])
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curriculum not found"
        )
    
    return {"message": "Curriculum deleted successfully"} 