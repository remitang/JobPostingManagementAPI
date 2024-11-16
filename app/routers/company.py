from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.company import Company, CompanyCreate, CompanyResponse
from ..models.user import User
from ..auth import get_current_user

router = APIRouter()

@router.post("/", response_model=CompanyResponse)
def create_company(company_data: CompanyCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):    # Vérifie que l'utilisateur a le droit de créer une entreprise
    if current_user.role <= 0:
        raise HTTPException(status_code=403, detail="You do not have permission to create a company")
    
    company = Company(**company_data.dict())
    company.list_of_recruiter = [current_user.id]
    db.add(company)
    db.commit()
    db.refresh(company)
    return company

@router.get("/{company_id}", response_model=CompanyResponse)
def read_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.get("/", response_model=list[CompanyResponse])
def read_companies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    companies = db.query(Company).offset(skip).limit(limit).all()
    return companies

@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(company_id: int, company_data: CompanyCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Vérifie que l'utilisateur a le droit d'accéder
    if current_user.role < 1:
        raise HTTPException(status_code=403, detail="Operation not permitted")

    company = db.query(Company).filter(Company.id == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    # Vérifie que l'utilisateur a le droit de mettre à jour l'entreprise
    if not (current_user.role == 2 or (current_user.role == 1 and current_user.id in company.list_of_recruiter)):
        raise HTTPException(status_code=403, detail="Operation not permitted")
    
    # Mise à jour des informations de l'entreprise
    for key, value in company_data.dict().items():
        setattr(company, key, value)
    db.commit()
    db.refresh(company)
    return company

@router.delete("/{company_id}", response_model=CompanyResponse)
def delete_company(company_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Vérifie que l'utilisateur a le droit d'accéder
    if current_user.role < 1:
        raise HTTPException(status_code=403, detail="Operation not permitted")

    company = db.query(Company).filter(Company.id == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    # Vérifie que l'utilisateur a le droit de supprimer l'entreprise
    if not (current_user.role == 2 or (current_user.role == 1 and current_user.id in company.list_of_recruiter)):
        raise HTTPException(status_code=403, detail="Operation not permitted")
    
    db.delete(company)
    db.commit()
    return company