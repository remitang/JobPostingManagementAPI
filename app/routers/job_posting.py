from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.job_posting import JobPosting, JobPostingCreate, JobPostingResponse
from ..models.user import User
from ..models.company import Company
from ..auth import get_current_user
from pydantic import BaseModel
from datetime import datetime
import json

router = APIRouter()


@router.post("/", response_model=JobPostingResponse)
def create_job_posting(job_posting_data: JobPostingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Vérifie que l'utilisateur a le droit de créer un job posting
    is_recruiter = current_user.role == 1
    is_admin = current_user.role == 2
    is_authorized_recruiter = is_recruiter and current_user.id in db.query(Company.list_of_recruiter).filter(Company.id == job_posting_data.company_id).first()[0]

    if not (is_admin or is_authorized_recruiter):
        raise HTTPException(status_code=403, detail="Operation not permitted")

    # Récupère l'entreprise associée
    company = db.query(Company).filter(Company.id == job_posting_data.company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Création de l'offre d'emploi
    job_posting = JobPosting(**job_posting_data.dict())
    db.add(job_posting)
    db.commit()  # Enregistre l'offre d'emploi pour générer l'ID

    # Récupère l'ID généré de l'offre d'emploi
    db.refresh(job_posting)  # Récupère les données actualisées de l'offre d'emploi
    

    company.list_of_job_posting.append(job_posting.id)
    company.number_of_job_posting += 1
    db.commit()  # Enregistre les modifications de la société
    
    return job_posting


@router.get("/{job_posting_id}", response_model=JobPostingResponse)
def read_job_posting(job_posting_id: int, db: Session = Depends(get_db)):
    job_posting = db.query(JobPosting).filter(JobPosting.id == job_posting_id).first()
    if job_posting is None:
        raise HTTPException(status_code=404, detail="Job Posting not found")
    return job_posting

@router.get("/", response_model=list[JobPostingResponse])
def read_job_postings(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    job_postings = db.query(JobPosting).offset(skip).limit(limit).all()
    return job_postings


@router.put("/{job_posting_id}", response_model=JobPostingResponse)
def update_job_posting(job_posting_id: int, job_posting_data: JobPostingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Vérifie que l'utilisateur a le droit de mettre à jour un job posting
    is_recruiter = current_user.role == 1
    is_admin = current_user.role == 2

    # Vérifie si l'utilisateur est un recruteur autorisé pour l'entreprise
    company = db.query(Company).filter(Company.id == job_posting_data.company_id).first()
    if company and is_recruiter:
        if current_user.id not in company.list_of_recruiter:
            raise HTTPException(status_code=403, detail="Operation not permitted")

    if not (is_admin or (is_recruiter and company)):
        raise HTTPException(status_code=403, detail="Operation not permitted")

    # Récupération de l'offre d'emploi à mettre à jour
    job_posting = db.query(JobPosting).filter(JobPosting.id == job_posting_id).first()
    if job_posting is None:
        raise HTTPException(status_code=404, detail="Job posting not found")

    # Mise à jour des données de l'offre d'emploi
    for key, value in job_posting_data.dict().items():
        setattr(job_posting, key, value)

    db.commit()  # Enregistre les modifications
    db.refresh(job_posting)  # Récupère les données actualisées
    return job_posting


@router.delete("/{job_posting_id}", response_model=JobPostingResponse)
def delete_job_posting(job_posting_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Vérifie que l'utilisateur a le droit de supprimer un job posting
    is_recruiter = current_user.role == 1
    is_admin = current_user.role == 2

    # Récupération de l'offre d'emploi à supprimer
    job_posting = db.query(JobPosting).filter(JobPosting.id == job_posting_id).first()
    if job_posting is None:
        raise HTTPException(status_code=404, detail="Job posting not found")

    company = db.query(Company).filter(Company.id == job_posting.company_id).first()
    if company and is_recruiter:
        if current_user.id not in company.list_of_recruiter:
            raise HTTPException(status_code=403, detail="Operation not permitted")

    if not (is_admin or (is_recruiter and company)):
        raise HTTPException(status_code=403, detail="Operation not permitted")

    # Suppression de l'offre d'emploi
    db.delete(job_posting)
    db.commit()  # Enregistre les modifications
    return job_posting