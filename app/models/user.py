"""
Modelo de Usuario
"""

from werkzeug.security import generate_password_hash, check_password_hash
from app.models.database import Database


class User:
    """Modelo para gestionar usuarios."""
    
    def __init__(self, id=None, username=None, email=None, password_hash=None,
                 first_name=None, last_name=None, birth_date=None, gender=None,
                 height_cm=None, created_at=None, updated_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.gender = gender
        self.height_cm = height_cm
        self.created_at = created_at
        self.updated_at = updated_at
    
    def set_password(self, password):
        """Genera el hash de la contraseña."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica la contraseña."""
        return check_password_hash(self.password_hash, password)
    
    def save(self):
        """Guarda o actualiza el usuario en la base de datos."""
        if self.id is None:
            query = """
                INSERT INTO users (username, email, password_hash, first_name, 
                                   last_name, birth_date, gender, height_cm)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (self.username, self.email, self.password_hash, 
                     self.first_name, self.last_name, self.birth_date,
                     self.gender, self.height_cm)
            self.id = Database.execute_insert(query, params)
        else:
            query = """
                UPDATE users 
                SET username=%s, email=%s, first_name=%s, last_name=%s,
                    birth_date=%s, gender=%s, height_cm=%s
                WHERE id=%s
            """
            params = (self.username, self.email, self.first_name, 
                     self.last_name, self.birth_date, self.gender, 
                     self.height_cm, self.id)
            Database.execute_update(query, params)
        return self
    
    @classmethod
    def get_by_id(cls, user_id):
        """Obtiene un usuario por su ID."""
        query = "SELECT * FROM users WHERE id = %s"
        result = Database.execute_query(query, (user_id,), fetch_one=True)
        if result:
            return cls(**result)
        return None
    
    @classmethod
    def get_by_username(cls, username):
        """Obtiene un usuario por su username."""
        query = "SELECT * FROM users WHERE username = %s"
        result = Database.execute_query(query, (username,), fetch_one=True)
        if result:
            return cls(**result)
        return None
    
    @classmethod
    def get_by_email(cls, email):
        """Obtiene un usuario por su email."""
        query = "SELECT * FROM users WHERE email = %s"
        result = Database.execute_query(query, (email,), fetch_one=True)
        if result:
            return cls(**result)
        return None
    
    def to_dict(self):
        """Convierte el usuario a diccionario."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': str(self.birth_date) if self.birth_date else None,
            'gender': self.gender,
            'height_cm': float(self.height_cm) if self.height_cm else None
        }
