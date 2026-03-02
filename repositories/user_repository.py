# repositories/user_repository.py
from models import User

class UserRepository:
    """SOLO consultas a la base de datos"""
    
    def get_by_username(self, db, username):
        """Buscar usuario por nombre de usuario"""
        return db.query(User).filter(User.username == username).first()
    
    def get_by_id(self, db, user_id):
        """Buscar usuario por ID"""
        return db.query(User).filter(User.idUser == user_id).first()
    
    def create(self, db, username, hashed_password):
        """Crear nuevo usuario"""
        user = User(
            username=username,
            passwd=hashed_password
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def username_exists(self, db, username):
        """Verificar si un username ya existe"""
        return db.query(User).filter(User.username == username).first() is not None