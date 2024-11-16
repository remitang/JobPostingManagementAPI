from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, ARRAY
from sqlalchemy.orm import relationship
from ..database import Base
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    website = Column(String)
    address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    list_of_recruiter = Column(ARRAY(Integer), default=[])
    list_of_job_posting = Column(ARRAY(Integer), default=[])
    number_of_job_posting = Column(Integer, default=0)

class CompanyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None

class CompanyResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]  # Permettre None
    website: Optional[str]      # Permettre None
    address: Optional[str]      # Permettre None
    created_at: datetime
    list_of_job_posting: Optional[List[int]]
    number_of_job_posting: Optional[int]

    class Config:
        orm_mode = True
