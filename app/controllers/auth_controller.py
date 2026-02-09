"""
Controlador de perfil de usuario
Aplicación de escritorio local (sin autenticación)
"""

from flask import Blueprint, request, render_template, flash
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

# ID de usuario local fijo
LOCAL_USER_ID = 1


@auth_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    """Perfil de usuario local."""
    user = User.get_by_id(LOCAL_USER_ID)
    
    # Si no existe el usuario, crear uno por defecto
    if not user:
        user = User(username="Usuario", email="usuario@local.app")
        user.set_password("local")
        user.id = LOCAL_USER_ID
        user.save()
        user = User.get_by_id(LOCAL_USER_ID)
    
    if request.method == 'POST':
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.birth_date = request.form.get('birth_date') or None
        user.gender = request.form.get('gender') or None
        user.height_cm = request.form.get('height_cm') or None
        user.save()
        
        flash('Perfil actualizado correctamente', 'success')
    
    return render_template('auth/profile.html', user=user)
