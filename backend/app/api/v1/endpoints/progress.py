from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user
from app.schemas.curriculum import ProgressUpdate
from app.services.progress_service import ProgressService
from typing import Dict, Any

router = APIRouter()

@router.post("/update")
def update_progress(
    progress_data: ProgressUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update the progress of a learning resource"""
    try:
        progress_service = ProgressService(db)
        success = progress_service.update_resource_status(
            resource_id=progress_data.resource_id,
            status=progress_data.status,
            user_id=current_user["user_id"]
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found or access denied"
            )
        
        return {"message": "Progress updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update progress: {str(e)}"
        )

@router.get("/summary")
def get_progress_summary(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a summary of the user's learning progress"""
    try:
        progress_service = ProgressService(db)
        summary = progress_service.get_progress_summary(current_user["user_id"])
        return summary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get progress summary: {str(e)}"
        ) 