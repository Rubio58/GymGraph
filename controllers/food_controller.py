# controllers/food_controller.py
from flask import jsonify, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from services.food_service import FoodService

food_bp = Blueprint('food', __name__, url_prefix='/food')

@food_bp.route('/create-food', methods=['POST'])
@login_required
def create_food():
    """Crear nuevo alimento"""
    name = request.form.get('name')

    if not name:
        flash('El nombre es obligatorio', 'error')
        return redirect(url_for('macros.index'))
        
    try:
        protein = float(request.form.get('protein', 0))
        carbs = float(request.form.get('carbs', 0))
        fats = float(request.form.get('fats', 0))

        if protein < 0 or carbs < 0 or fats < 0:
            return {'success': False, 'error': 'Los valores no pueden ser negativos'}
        
    except ValueError:
        flash('Los valores deben ser números', 'error')
        return redirect(url_for('macros.index'))
    

    service = FoodService()
    result = service.create_food(current_user.id , name, protein, carbs, fats)
    
    if result['success']:
        flash('Alimento creado exitosamente', 'success')
    else:
        flash(result['error'], 'error')
    
    return redirect(url_for('macros.index'))

@food_bp.route('/create-meal', methods=['POST'])
@login_required
def create_meal():

    foods_data = []
    i=0

    if not request.form.get('food_id_0') or not request.form.get('grams_0'):
        flash('Debes añadir al menos un alimento a la comida', 'error')
        return redirect(url_for('macros.index'))
    
    while True:
        food_id = request.form.get(f'food_id_{i}')
        grams = request.form.get(f'grams_{i}')
        
        if not food_id or not grams:
            break
            
        try:
            foods_data.append({
                'food_id': int(food_id),
                'grams': float(grams)
            })
        except ValueError:
            flash(f'Valores inválidos en el alimento {i+1}', 'error')
            return redirect(url_for('macros.index'))
        
        i += 1

    service = FoodService()
    result = service.create_meal(current_user.id, foods_data)
    
    if result['success']:
        flash('Comida creada exitosamente', 'success')
    else:
        flash(result['error'], 'error')    

    return redirect(url_for('macros.index'))

@food_bp.route('/delete-meal/<int:meal_id>', methods=['POST'])
@login_required
def delete_meal(meal_id):

    """Eliminar una comida"""

    service = FoodService()
    result = service.delete_meal(meal_id)
    
    if result['success']:
        flash('Comida eliminada correctamente', 'success')
    else:
        flash(result['error'], 'error')
    
    return redirect(url_for('macros.index'))  

@food_bp.route('/update-meal/<int:meal_id>', methods=['POST'])
@login_required
def update_meal(meal_id):
    food_service = FoodService()
    
    # Procesar la edición
    foods_data = []
    i = 0
    
    while f'food_{i}' in request.form:
        food_id = request.form.get(f'food_{i}')
        grams = request.form.get(f'grams_{i}')
        meal_food_id = request.form.get(f'meal_food_id_{i}')
        
        if food_id and grams:
            try:
                food_item = {
                    'food_id': int(food_id),
                    'grams': float(grams)
                }
                
                # Si tiene meal_food_id, es un alimento existente
                if meal_food_id:
                    food_item['id'] = int(meal_food_id)
                
                foods_data.append(food_item)
            except ValueError:
                return jsonify({'success': False, 'error': f'Valores inválidos en el alimento {i+1}'})
        
        i += 1
    
    if not foods_data:
        flash('Debe haber al menos un alimento', 'error')
        return redirect(url_for('macros.index'))
    
    result = food_service.update_meal(
        meal_id=meal_id,
        user_id=current_user.id,
        foods_data=foods_data
    )

    if result['success']:
        flash('Comida actualizada correctamente', 'success')
    else:
        flash(result['error'], 'error')

    return redirect(url_for('macros.index'))
