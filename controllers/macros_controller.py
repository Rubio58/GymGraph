# controllers/macros_controller.py
from flask import render_template, request, redirect, url_for, flash, Blueprint, jsonify
from flask_login import login_required, current_user
from services.food_service import FoodService
from services.macros_service import MacrosService
from datetime import datetime, timedelta

macros_bp = Blueprint('macros', __name__, url_prefix='/macros')

@macros_bp.route('/')
@login_required
def index():
    """Página principal de macros"""
    food_service = FoodService()
    macros_service = MacrosService()
    
    # Obtener fecha de la query string o usar hoy
    date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    try:
        # Crear objeto datetime para pasar al servicio
        current_date = datetime.strptime(date_str, '%Y-%m-%d')
        # También necesitamos la versión string para el template
        current_date_str = current_date.strftime('%Y-%m-%d')
    except ValueError:
        current_date = datetime.now()
        current_date_str = current_date.strftime('%Y-%m-%d')
    
    # Calcular fechas anterior y siguiente (en string para los links)
    prev_date = (current_date - timedelta(days=1)).strftime('%Y-%m-%d')
    next_date = (current_date + timedelta(days=1)).strftime('%Y-%m-%d')
    today_str = datetime.now().strftime('%Y-%m-%d')
    
    # Determinar si el botón "siguiente" debe estar habilitado
    can_go_next = current_date.date() < datetime.now().date()
    
    # Datos para la vista - PASAMOS EL OBJETO DATETIME
    foods = food_service.get_user_foods(current_user.id)
    meals = macros_service.get_meals_by_date(current_user.id, current_date)  # ← Ahora pasamos datetime
    totals = macros_service.get_daily_totals(current_user.id, current_date)   # ← Ahora pasamos datetime
    
    return render_template(
        'macros/index.html',
        foods=foods,
        meals=meals,
        totals=totals,
        current_date=current_date_str,  # Para mostrar en el template
        prev_date=prev_date,
        next_date=next_date,
        can_go_next=can_go_next,
        today=today_str
    )

  