"""
Controlador de Entrenamiento
"""

from flask import Blueprint, request, render_template, redirect, url_for, session, flash, jsonify
from datetime import date, datetime
# Sin autenticación - aplicación local
from app.models.workout import (
    Exercise, TrainingPlan, TrainingDay, 
    PlannedExercise, WorkoutSession, WorkoutSet
)

workout_bp = Blueprint('workout', __name__)


# ============================================
# VISTAS HTML
# ============================================

@workout_bp.route('/plans')

def plans():
    """Vista de planes de entrenamiento."""
    user_id = session['user_id']
    training_plans = TrainingPlan.get_by_user(user_id)
    return render_template('workout/plans.html', plans=training_plans)


@workout_bp.route('/plans/new', methods=['GET', 'POST'])

def new_plan():
    """Crear nuevo plan de entrenamiento."""
    if request.method == 'POST':
        user_id = session['user_id']
        name = request.form.get('name')
        description = request.form.get('description')
        
        plan = TrainingPlan(user_id=user_id, name=name, description=description)
        plan.save()
        
        flash('Plan creado correctamente', 'success')
        return redirect(url_for('workout.edit_plan', plan_id=plan.id))
    
    return render_template('workout/new_plan.html')


@workout_bp.route('/plans/<int:plan_id>')

def edit_plan(plan_id):
    """Editar plan de entrenamiento."""
    exercises = Exercise.get_all(session['user_id'])
    return render_template('workout/edit_plan.html', 
                         plan_id=plan_id, exercises=exercises)


@workout_bp.route('/session')

def workout_session():
    """Vista de sesión de entrenamiento activa."""
    user_id = session['user_id']
    active_plan = TrainingPlan.get_active_plan(user_id)
    exercises = Exercise.get_all(user_id)
    
    return render_template('workout/session.html', 
                         plan=active_plan, exercises=exercises)


@workout_bp.route('/history')

def history():
    """Historial de entrenamientos."""
    user_id = session['user_id']
    sessions = WorkoutSession.get_by_user(user_id, limit=20)
    return render_template('workout/history.html', sessions=sessions)


# ============================================
# API ENDPOINTS
# ============================================

@workout_bp.route('/api/exercises')

def api_exercises():
    """API: Obtener ejercicios."""
    user_id = session['user_id']
    muscle_group = request.args.get('muscle_group')
    
    if muscle_group:
        exercises = Exercise.get_by_muscle_group(muscle_group, user_id)
    else:
        exercises = Exercise.get_all(user_id)
    
    return jsonify([ex.to_dict() for ex in exercises])


@workout_bp.route('/api/exercises', methods=['POST'])

def api_create_exercise():
    """API: Crear ejercicio personalizado."""
    data = request.json
    user_id = session['user_id']
    
    exercise = Exercise(
        name=data['name'],
        description=data.get('description'),
        muscle_group=data.get('muscle_group'),
        equipment=data.get('equipment'),
        created_by=user_id,
        is_custom=True
    )
    exercise.save()
    
    return jsonify(exercise.to_dict()), 201


@workout_bp.route('/api/plans')

def api_plans():
    """API: Obtener planes."""
    user_id = session['user_id']
    plans = TrainingPlan.get_by_user(user_id)
    return jsonify([p.to_dict() for p in plans])


@workout_bp.route('/api/plans/<int:plan_id>')

def api_plan_detail(plan_id):
    """API: Obtener detalle de un plan."""
    query = "SELECT * FROM training_plans WHERE id = %s"
    from app.models.database import Database
    result = Database.execute_query(query, (plan_id,), fetch_one=True)
    
    if result and result['user_id'] == session['user_id']:
        plan = TrainingPlan(**result)
        return jsonify(plan.to_dict())
    
    return jsonify({'error': 'Plan no encontrado'}), 404


@workout_bp.route('/api/plans/<int:plan_id>/days', methods=['POST'])

def api_add_day(plan_id):
    """API: Añadir día al plan."""
    data = request.json
    
    day = TrainingDay(
        plan_id=plan_id,
        day_of_week=data['day_of_week'],
        name=data.get('name')
    )
    day.save()
    
    return jsonify(day.to_dict()), 201


@workout_bp.route('/api/days/<int:day_id>/exercises', methods=['POST'])

def api_add_exercise_to_day(day_id):
    """API: Añadir ejercicio a un día."""
    data = request.json
    
    planned = PlannedExercise(
        training_day_id=day_id,
        exercise_id=data['exercise_id'],
        order_index=data.get('order_index', 0),
        target_sets=data.get('target_sets'),
        target_reps=data.get('target_reps'),
        notes=data.get('notes')
    )
    planned.save()
    
    return jsonify(planned.to_dict()), 201


@workout_bp.route('/api/sessions', methods=['POST'])

def api_start_session():
    """API: Iniciar sesión de entrenamiento."""
    data = request.json
    user_id = session['user_id']
    
    workout_session = WorkoutSession(
        user_id=user_id,
        training_day_id=data.get('training_day_id'),
        session_date=date.today(),
        start_time=datetime.now().time()
    )
    workout_session.save()
    
    return jsonify(workout_session.to_dict()), 201


@workout_bp.route('/api/sessions/<int:session_id>/sets', methods=['POST'])

def api_add_set(session_id):
    """API: Registrar serie."""
    data = request.json
    
    workout_set = WorkoutSet(
        session_id=session_id,
        exercise_id=data['exercise_id'],
        set_number=data['set_number'],
        weight_kg=data.get('weight_kg'),
        reps=data.get('reps'),
        rpe=data.get('rpe'),
        is_warmup=data.get('is_warmup', False),
        notes=data.get('notes')
    )
    workout_set.save()
    
    return jsonify(workout_set.to_dict()), 201


@workout_bp.route('/api/sessions/<int:session_id>/end', methods=['POST'])

def api_end_session(session_id):
    """API: Finalizar sesión."""
    from app.models.database import Database
    
    query = "UPDATE workout_sessions SET end_time = %s WHERE id = %s"
    Database.execute_update(query, (datetime.now().time(), session_id))
    
    return jsonify({'message': 'Sesión finalizada'})


@workout_bp.route('/api/exercises/<int:exercise_id>/history')

def api_exercise_history(exercise_id):
    """API: Historial de un ejercicio."""
    user_id = session['user_id']
    history = WorkoutSet.get_exercise_history(user_id, exercise_id)
    return jsonify(history)


@workout_bp.route('/api/sessions/latest')

def api_latest_session():
    """API: Último entrenamiento."""
    user_id = session['user_id']
    latest = WorkoutSession.get_latest(user_id)
    if latest:
        return jsonify(latest.to_dict())
    return jsonify({})
