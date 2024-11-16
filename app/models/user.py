from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from ..database import Base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, ConfigDict
from datetime import datetime


# Modèle SQLAlchemy
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(Integer, default=0)  # 0: candidate, 1: recruiter, 2: admin
    name = Column(String)
    address = Column(String)
    telephone = Column(String)
    cv = Column(String)
    creation_date = Column(DateTime, default=datetime.utcnow)

# Modèle Pydantic pour la création d'utilisateur
class UserCreate(BaseModel):
    email: str
    password: str

# Modèle Pydantic pour la connexion
class UserLogin(BaseModel):
    email: str
    password: str

# Modèle Pydantic pour la réponse d'utilisateur
class UserResponse(BaseModel):
    id: int
    email: str
    model_config = ConfigDict(from_attributes=True)
