from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://gymgraph:cambrita2024@localhost/gymgraph')

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

