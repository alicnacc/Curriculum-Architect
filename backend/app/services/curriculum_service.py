from sqlalchemy.orm import Session
from app.models.curriculum import Curriculum, CurriculumModule, LearningResource
from app.schemas.curriculum import CurriculumCreate, CurriculumResponse, CurriculumComplete
from typing import List, Optional

class CurriculumService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_curriculums(self, user_id: int) -> List[Curriculum]:
        """Get all curriculums for a user"""
        return self.db.query(Curriculum).filter(Curriculum.user_id == user_id).all()
    
    def get_curriculum_with_modules(self, curriculum_id: int, user_id: int) -> Optional[Curriculum]:
        """Get a curriculum with all its modules and resources"""
        return self.db.query(Curriculum).filter(
            Curriculum.id == curriculum_id,
            Curriculum.user_id == user_id
        ).first()
    
    def create_curriculum(self, user_id: int, curriculum_data: CurriculumCreate) -> Curriculum:
        """Create a new curriculum"""
        curriculum = Curriculum(
            user_id=user_id,
            title=curriculum_data.title,
            description=curriculum_data.description
        )
        self.db.add(curriculum)
        self.db.commit()
        self.db.refresh(curriculum)
        return curriculum
    
    def create_module(self, curriculum_id: int, title: str, description: str = None, order: int = 0) -> CurriculumModule:
        """Create a new module for a curriculum"""
        module = CurriculumModule(
            curriculum_id=curriculum_id,
            title=title,
            description=description,
            order=order
        )
        self.db.add(module)
        self.db.commit()
        self.db.refresh(module)
        return module
    
    def create_resource(self, module_id: int, title: str, url: str, resource_type: str, description: str = None, order: int = 0) -> LearningResource:
        """Create a new learning resource"""
        resource = LearningResource(
            module_id=module_id,
            title=title,
            description=description,
            url=url,
            resource_type=resource_type,
            order=order
        )
        self.db.add(resource)
        self.db.commit()
        self.db.refresh(resource)
        return resource
    
    def delete_curriculum(self, curriculum_id: int, user_id: int) -> bool:
        """Delete a curriculum"""
        curriculum = self.db.query(Curriculum).filter(
            Curriculum.id == curriculum_id,
            Curriculum.user_id == user_id
        ).first()
        
        if curriculum:
            self.db.delete(curriculum)
            self.db.commit()
            return True
        return False 