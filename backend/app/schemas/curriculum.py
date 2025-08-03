from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.curriculum import ResourceType, ResourceStatus

class CurriculumBase(BaseModel):
    title: str
    description: Optional[str] = None

class CurriculumCreate(CurriculumBase):
    pass

class CurriculumResponse(CurriculumBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ModuleBase(BaseModel):
    title: str
    description: Optional[str] = None
    order: int

class ModuleCreate(ModuleBase):
    pass

class ModuleResponse(ModuleBase):
    id: int
    curriculum_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ResourceBase(BaseModel):
    title: str
    description: Optional[str] = None
    url: str
    resource_type: ResourceType
    order: int

class ResourceCreate(ResourceBase):
    pass

class ResourceUpdate(BaseModel):
    status: ResourceStatus

class ResourceResponse(ResourceBase):
    id: int
    module_id: int
    status: ResourceStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class CurriculumWithModules(CurriculumResponse):
    modules: List[ModuleResponse] = []

class ModuleWithResources(ModuleResponse):
    resources: List[ResourceResponse] = []

class CurriculumComplete(CurriculumResponse):
    modules: List[ModuleWithResources] = []

class ProgressUpdate(BaseModel):
    resource_id: int
    status: ResourceStatus 