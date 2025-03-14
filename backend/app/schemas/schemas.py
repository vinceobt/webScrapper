from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from app.models.models import TaskStatus

class ScrapingTaskBase(BaseModel):
    url: HttpUrl = Field(..., description="URL to scrape")

class ScrapingTaskCreate(ScrapingTaskBase):
    pass

class ScrapingTaskResponse(ScrapingTaskBase):
    id: int
    status: TaskStatus
    created_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    
    class Config:
        orm_mode = True

class ScrapingResultBase(BaseModel):
    content: Optional[Dict[str, Any]] = None
    html_content: Optional[str] = None

class ScrapingResultCreate(ScrapingResultBase):
    task_id: int

class ScrapingResultResponse(ScrapingResultBase):
    id: int
    task_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class TaskWithResults(ScrapingTaskResponse):
    results: List[ScrapingResultResponse] = []
    
    class Config:
        orm_mode = True

class TaskStatusUpdate(BaseModel):
    status: TaskStatus
    error_message: Optional[str] = None