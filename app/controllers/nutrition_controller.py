"""
Controlador de Nutrición
"""

from flask import Blueprint, request, render_template, redirect, url_for, session, flash, jsonify
from datetime import date
# Sin autenticación - aplicación local
from app.models.nutrition import Food, NutritionGoal, FoodLog, WaterLog

nutrition_bp = Blueprint('nutrition', __name__)


# ============================================
# VISTAS HTML
# ============================================

@nutrition_bp.route('/')

def index():
    """Vista principal de nutrición."""
    user_id = session['user_id']
    today = date.today()
    
    # Obtener datos del día
    food_logs = FoodLog.get_by_date(user_id, today)
    totals = FoodLog.get_daily_totals(user_id, today)
    water_log = WaterLog.get_by_date(user_id, today)
    goals = NutritionGoal.get_by_user(user_id)
    
    return render_template('nutrition/index.html',
                         food_logs=food_logs,
                         totals=totals,
                         water_log=water_log,
                         goals=goals,
                         today=today)


@nutrition_bp.route('/foods')

def foods():
    """Catálogo de alimentos."""
    user_id = session['user_id']
    foods_list = Food.get_all(user_id)
    return render_template('nutrition/foods.html', foods=foods_list)


@nutrition_bp.route('/foods/new', methods=['GET', 'POST'])

def new_food():
    """Crear nuevo alimento."""
    if request.method == 'POST':
        user_id = session['user_id']
        
        food = Food(
            user_id=user_id,
            name=request.form.get('name'),
            brand=request.form.get('brand'),
            serving_size=float(request.form.get('serving_size', 100)),
            serving_unit=request.form.get('serving_unit', 'g'),
            calories=float(request.form.get('calories', 0)),
            protein_g=float(request.form.get('protein_g', 0)),
            carbs_g=float(request.form.get('carbs_g', 0)),
            fat_g=float(request.form.get('fat_g', 0)),
            fiber_g=float(request.form.get('fiber_g', 0)),
            is_custom=True
        )
        food.save()
        
        flash('Alimento guardado correctamente', 'success')
        return redirect(url_for('nutrition.foods'))
    
    return render_template('nutrition/new_food.html')


@nutrition_bp.route('/goals', methods=['GET', 'POST'])

def goals():
    """Configurar objetivos nutricionales."""
    user_id = session['user_id']
    current_goals = NutritionGoal.get_by_user(user_id)
    
    if request.method == 'POST':
        goals = NutritionGoal(
            user_id=user_id,
            daily_calories=int(request.form.get('daily_calories') or 0),
            protein_g=int(request.form.get('protein_g') or 0),
            carbs_g=int(request.form.get('carbs_g') or 0),
            fat_g=int(request.form.get('fat_g') or 0),
            water_liters=float(request.form.get('water_liters') or 0)
        )
        goals.save()
        
        flash('Objetivos actualizados', 'success')
        return redirect(url_for('nutrition.index'))
    
    return render_template('nutrition/goals.html', goals=current_goals)


# ============================================
# API ENDPOINTS
# ============================================

@nutrition_bp.route('/api/foods')

def api_foods():
    """API: Buscar alimentos."""
    user_id = session['user_id']
    search = request.args.get('q', '')
    
    if search:
        foods = Food.search(search, user_id)
    else:
        foods = Food.get_all(user_id)
    
    return jsonify([f.to_dict() for f in foods])


@nutrition_bp.route('/api/foods', methods=['POST'])

def api_create_food():
    """API: Crear alimento."""
    data = request.json
    user_id = session['user_id']
    
    food = Food(
        user_id=user_id,
        name=data['name'],
        brand=data.get('brand'),
        serving_size=data.get('serving_size', 100),
        serving_unit=data.get('serving_unit', 'g'),
        calories=data.get('calories', 0),
        protein_g=data.get('protein_g', 0),
        carbs_g=data.get('carbs_g', 0),
        fat_g=data.get('fat_g', 0),
        fiber_g=data.get('fiber_g', 0),
        is_custom=True
    )
    food.save()
    
    return jsonify(food.to_dict()), 201


@nutrition_bp.route('/api/logs', methods=['POST'])

def api_add_food_log():
    """API: Registrar alimento consumido."""
    data = request.json
    user_id = session['user_id']
    
    log = FoodLog(
        user_id=user_id,
        food_id=data['food_id'],
        log_date=data.get('log_date', date.today().isoformat()),
        meal_type=data['meal_type'],
        quantity=data['quantity'],
        unit=data.get('unit', 'g')
    )
    log.save()
    
    return jsonify({'message': 'Registro guardado', 'id': log.id}), 201


@nutrition_bp.route('/api/logs/<int:log_id>', methods=['DELETE'])

def api_delete_food_log(log_id):
    """API: Eliminar registro."""
    log = FoodLog(id=log_id)
    log.delete()
    return jsonify({'message': 'Registro eliminado'})


@nutrition_bp.route('/api/logs/<string:log_date>')

def api_get_logs(log_date):
    """API: Obtener registros de un día."""
    user_id = session['user_id']
    logs = FoodLog.get_by_date(user_id, log_date)
    totals = FoodLog.get_daily_totals(user_id, log_date)
    
    return jsonify({
        'logs': logs,
        'totals': totals
    })


@nutrition_bp.route('/api/water', methods=['POST'])

def api_add_water():
    """API: Registrar agua."""
    data = request.json
    user_id = session['user_id']
    log_date = data.get('log_date', date.today().isoformat())
    liters = float(data['liters'])
    
    WaterLog.add_water(user_id, log_date, liters)
    
    return jsonify({'message': 'Agua registrada'})


@nutrition_bp.route('/api/water/<string:log_date>')

def api_get_water(log_date):
    """API: Obtener agua del día."""
    user_id = session['user_id']
    water_log = WaterLog.get_by_date(user_id, log_date)
    
    return jsonify({
        'liters': float(water_log.liters) if water_log else 0
    })


@nutrition_bp.route('/api/goals')

def api_get_goals():
    """API: Obtener objetivos."""
    user_id = session['user_id']
    goals = NutritionGoal.get_by_user(user_id)
    
    if goals:
        return jsonify(goals.to_dict())
    return jsonify({})


@nutrition_bp.route('/api/calories-history')

def api_calories_history():
    """API: Obtener historial de calorías (últimos días)."""
    from datetime import timedelta
    from app.models.database import Database
    
    user_id = session['user_id']
    days = int(request.args.get('days', 7))
    
    end_date = date.today()
    start_date = end_date - timedelta(days=days-1)
    
    query = """
        SELECT fl.log_date, SUM(f.calories * fl.quantity) as total_calories
        FROM food_logs fl
        JOIN foods f ON fl.food_id = f.id
        WHERE fl.user_id = ? AND fl.log_date >= ? AND fl.log_date <= ?
        GROUP BY fl.log_date
        ORDER BY fl.log_date
    """
    results = Database.execute_query(query, (user_id, start_date.isoformat(), end_date.isoformat()))
    
    return jsonify([
        {'log_date': row['log_date'], 'calories': row['total_calories'] or 0}
        for row in results
    ])
