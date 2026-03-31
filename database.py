#database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# Cargar variables de entorno
load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')

engine = create_engine(DATABASE_URL,echo=True,)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    """Context manager para sesiones de BD"""
    db = SessionLocal()
    try:
        yield db
        db.commit()  # Auto-commit si todo OK
    except Exception as e:
        db.rollback()  # Auto-rollback si error
        print(f"Error en BD: {e}")
        raise
    finally:
        db.close()  # Auto-close SIEMPRE

