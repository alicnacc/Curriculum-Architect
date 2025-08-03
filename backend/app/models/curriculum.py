from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class ResourceType(str, enum.Enum):
    VIDEO = "video"
    ARTICLE = "article"
    INTERACTIVE = "interactive"
    QUIZ = "quiz"
    SIMULATION = "simulation"

class ResourceStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"

class Curriculum(Base):
    __tablename__ = "curriculums"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    modules = relationship("CurriculumModule", back_populates="curriculum")

class CurriculumModule(Base):
    __tablename__ = "curriculum_modules"
    
    id = Column(Integer, primary_key=True, index=True)
    curriculum_id = Column(Integer, ForeignKey("curriculums.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    order = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    curriculum = relationship("Curriculum", back_populates="modules")
    resources = relationship("LearningResource", back_populates="module")

class LearningResource(Base):
    __tablename__ = "learning_resources"
    
    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("curriculum_modules.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String, nullable=False)
    resource_type = Column(Enum(ResourceType), nullable=False)
    status = Column(Enum(ResourceStatus), default=ResourceStatus.PENDING)
    order = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    module = relationship("CurriculumModule", back_populates="resources") 