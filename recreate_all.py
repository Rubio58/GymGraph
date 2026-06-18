# recreate_all.py
import os
from dotenv import load_dotenv
from app import app
from models import Base
from database import engine

load_dotenv()

print("⚠️  Esto BORRARÁ todos los datos de Aiven")
respuesta = input("¿Estás seguro? (escribe 'SI' para continuar): ")

if respuesta != 'SI':
    print("Cancelado")
    exit()

with app.app_context():
    print("Eliminando tablas...")
    Base.metadata.drop_all(bind=engine)
    print("Creando tablas con autoincrement...")
    Base.metadata.create_all(bind=engine)
    print("✅ Listo")