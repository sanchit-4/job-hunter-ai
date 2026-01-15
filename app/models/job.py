import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # CHANGED: Removed unique=True. 
    # Multiple users can now apply to the same URL.
    url = Column(String, index=True) 
    
    title = Column(String, nullable=True)
    company = Column(String, nullable=True)
    original_resume = Column(Text)
    
    raw_job_description = Column(Text, nullable=True)
    tailored_resume_content = Column(JSON, nullable=True)
    cover_letter = Column(Text, nullable=True)
    
    status = Column(String, default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow)