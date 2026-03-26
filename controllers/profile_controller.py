# controllers/profile_controller.py

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from services.user_service import UserService


profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/')
@login_required
def index():
    """Página principal de profile"""
    user_service=UserService()
    objectives=user_service.get_objectives_by_user(current_user.id)    
    return render_template(
        'profile/index.html',
        objectives=objectives
    )

@profile_bp.route('/update-objectives', methods=['POST'])
@login_required
def update_objectives():
    protein = request.form.get('protein')
    carbs = request.form.get('carbs')
    fats = request.form.get('fats')
    user_service=UserService()
    user_service.update_objectives(current_user.id, protein, carbs, fats)
    return redirect(url_for('profile.index'))

@profile_bp.route('/update-username', methods=['POST'])
@login_required
def update_username():
    username = request.form.get('username')

    user_service=UserService()
    user_service.update_username(current_user.id,username)
    return redirect(url_for('profile.index'))