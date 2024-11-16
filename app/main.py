from fastapi import FastAPI
from sqlalchemy.orm import Session
from .database import engine, get_db, Base
from .routers import job_posting, user, company

# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Routers de l'API
app.include_router(job_posting.router, prefix="/jobs", tags=["job_postings"])
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(company.router, prefix="/companies", tags=["companies"])