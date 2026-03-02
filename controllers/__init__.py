# controllers/__init__.py
from flask_login import UserMixin

class CurrentUser(UserMixin):
    """Wrapper para Flask-Login (disponible para todos los controllers)"""
    def __init__(self, user_model):
        self.id = user_model.idUser
        self.username = user_model.username