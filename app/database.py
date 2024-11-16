from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Chaîne de connexion PostgreSQL
DATABASE_URL = "[YOUR_DATABASE_URL]"

# Créer le moteur SQLAlchemy pour interagir avec PostgreSQL
engine = create_engine(DATABASE_URL)

# Base pour les modèles SQLAlchemy
Base = declarative_base()

# Créer une session locale pour interagir avec la base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fonction pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
