from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, ARRAY
from sqlalchemy.dialects.postgresql import JSON
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import relationship
from ..database import Base
from pydantic import BaseModel

class JobPosting(Base):
    __tablename__ = "job_posting"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    requirements = Column(String, nullable=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    address = Column(String, nullable=True)
    salary = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expiration_date = Column(DateTime, nullable=True)
    candidates_id = Column(ARRAY(Integer), default=[])
    number_of_candidats = Column(Integer, default=0)

class JobPostingCreate(BaseModel):
    title: str
    description: str
    requirements: Optional[str] = None
    company_id: int
    address: Optional[str] = None
    salary: Optional[float] = None
    expiration_date: Optional[datetime] = None

class JobPostingResponse(BaseModel):
    id: int
    title: str
    description: str
    requirements: Optional[str]
    company_id: int
    address: Optional[str]
    salary: Optional[float]
    created_at: datetime
    expiration_date: Optional[datetime]
    candidates_id: Optional[list[int]]
    number_of_candidats: int

    class Config:
        orm_mode = True
