#!/usr/bin/env python3
"""Script para inicializar la base de datos con las tablas"""

from database import engine
from models import Base

if __name__ == '__main__':
    print("🔄 Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ ¡Tablas creadas exitosamente!")
