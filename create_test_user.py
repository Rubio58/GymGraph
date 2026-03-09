#!/usr/bin/env python3
"""Script para crear un usuario de prueba"""

from werkzeug.security import generate_password_hash
from database import get_db
from repositories.user_repository import UserRepository

if __name__ == '__main__':
    username = 'demo'
    password = 'demo123'
    
    repo = UserRepository()
    
    try:
        with get_db() as db:
            # Comprobar si ya existe
            if repo.username_exists(db, username):
                print(f"⚠️  El usuario '{username}' ya existe")
            else:
                # Crear usuario
                hashed_password = generate_password_hash(password)
                user = repo.create(db, username, hashed_password)
                print(f"✅ Usuario de prueba creado:")
                print(f"   Usuario: {username}")
                print(f"   Contraseña: {password}")
    except Exception as e:
        print(f"❌ Error: {e}")
