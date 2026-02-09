"""
Inicialización de controladores
"""

from app.controllers.main_controller import main_bp
from app.controllers.auth_controller import auth_bp
from app.controllers.workout_controller import workout_bp
from app.controllers.nutrition_controller import nutrition_bp
from app.controllers.measurement_controller import measurement_bp
from app.controllers.selfcare_controller import selfcare_bp

__all__ = [
    'main_bp', 'auth_bp', 'workout_bp', 
    'nutrition_bp', 'measurement_bp', 'selfcare_bp'
]
