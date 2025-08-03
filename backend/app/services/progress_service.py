from sqlalchemy.orm import Session
from app.models.curriculum import LearningResource, ResourceStatus, Curriculum
from app.models.user import UserProfile
from typing import Dict, Any, Optional

class ProgressService:
    def __init__(self, db: Session):
        self.db = db
    
    def update_resource_status(self, resource_id: int, status: ResourceStatus, user_id: int) -> bool:
        """Update the status of a learning resource"""
        # Verify the resource belongs to the user
        resource = self.db.query(LearningResource).join(
            CurriculumModule
        ).join(
            Curriculum
        ).filter(
            LearningResource.id == resource_id,
            Curriculum.user_id == user_id
        ).first()
        
        if resource:
            resource.status = status
            self.db.commit()
            return True
        return False
    
    def get_progress_summary(self, user_id: int) -> Dict[str, Any]:
        """Get a summary of the user's learning progress"""
        # Get all resources for the user's curriculums
        resources = self.db.query(LearningResource).join(
            CurriculumModule
        ).join(
            Curriculum
        ).filter(
            Curriculum.user_id == user_id
        ).all()
        
        # Calculate statistics
        total_resources = len(resources)
        completed_resources = len([r for r in resources if r.status == ResourceStatus.COMPLETED])
        in_progress_resources = len([r for r in resources if r.status == ResourceStatus.IN_PROGRESS])
        pending_resources = len([r for r in resources if r.status == ResourceStatus.PENDING])
        
        # Calculate completion percentage
        completion_percentage = (completed_resources / total_resources * 100) if total_resources > 0 else 0
        
        # Get user profile for context
        profile = self.db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        
        return {
            "total_resources": total_resources,
            "completed_resources": completed_resources,
            "in_progress_resources": in_progress_resources,
            "pending_resources": pending_resources,
            "completion_percentage": round(completion_percentage, 2),
            "learning_style": profile.learning_style if profile else None,
            "pace": profile.pace if profile else None
        }
    
    def get_recent_progress(self, user_id: int, limit: int = 5) -> list:
        """Get recent progress updates"""
        resources = self.db.query(LearningResource).join(
            CurriculumModule
        ).join(
            Curriculum
        ).filter(
            Curriculum.user_id == user_id,
            LearningResource.status.in_([ResourceStatus.COMPLETED, ResourceStatus.IN_PROGRESS])
        ).order_by(
            LearningResource.updated_at.desc()
        ).limit(limit).all()
        
        return [
            {
                "id": resource.id,
                "title": resource.title,
                "status": resource.status,
                "updated_at": resource.updated_at,
                "module_title": resource.module.title
            }
            for resource in resources
        ] 