from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User, UserLogin, UserResponse, UserCreate
from ..auth import get_current_user, create_access_token, verify_password, hash_password
from passlib.context import CryptContext
from datetime import datetime

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Créer une instance de CryptContext pour le hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hacher le mot de passe
    hashed_password = pwd_context.hash(user_data.password)
    
    # Créer l'utilisateur avec des valeurs par défaut
    user = User(
        email=user_data.email,
        password=hashed_password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserResponse(id=user.id, email=user.email)


@router.post("/login")
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if user is None or not pwd_context.verify(user_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Vérifiez le token et récupérez l'utilisateur
    user = get_current_user(token, db)  # Implémentez cette fonction pour extraire l'utilisateur
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Vérification si l'utilisateur connecté est un admin ou l'utilisateur cible
    if current_user.role != 2 and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Suppression de l'utilisateur
    db.delete(user)
    db.commit()
    return {"detail": "User successfully deleted"}