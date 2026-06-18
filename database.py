# database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# Cargar variables de entorno (solo útil en local)
load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')

# Validación para detectar errores rápido
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL no está configurada en las variables de entorno")

# Si la URL viene de Aiven con ssl-mode, corregirla automáticamente
if 'ssl-mode' in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace('ssl-mode', 'ssl_ca')
    print("⚠️  Corregido 'ssl-mode' → 'ssl_ca' en DATABASE_URL")

print(f"🔗 Conectando a: {DATABASE_URL.split('@')[1].split('/')[0]}")  # Muestra host sin contraseña

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    """Context manager para sesiones de BD"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"❌ Error en BD: {e}")
        raise
    finally:
        db.close()
