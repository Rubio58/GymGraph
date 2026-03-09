#!/usr/bin/env python3
"""Script para recrear las tablas de la base de datos con la estructura corregida"""

from database import engine
from models import Base

# Eliminar todas las tablas existentes
print("Eliminando tablas existentes...")
Base.metadata.drop_all(engine)

# Crear las tablas nuevas con la estructura corregida
print("Creando tablas nuevas...")
Base.metadata.create_all(engine)

print("✅ Tablas recreadas correctamente")
