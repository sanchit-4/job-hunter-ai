from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID

class JobCreate(BaseModel):
    url: str
    original_resume_text: str

class JobResponse(BaseModel):
    id: UUID
    url: str
    status: str
    cover_letter: Optional[str] = None
    tailored_resume_content: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True