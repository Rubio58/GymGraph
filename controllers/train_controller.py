# controllers/train_controller.py
from datetime import datetime
from flask import  render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from services.train_service import TrainService

train_bp = Blueprint('train', __name__, url_prefix='/train')

@train_bp.route('/')
@login_required
def index():
    """Página principal de entrenamiento"""
    train_service = TrainService()
    trainplans = train_service.get_trainplans(current_user.id)
    
    return render_template(
        'train/index.html',
        trainplans=trainplans,
    )

@train_bp.route('/start-workout', methods=['POST'])
@login_required
def start_workout():
    """Redirige a ventana workout"""
    trainday_id = request.form.get('trainday_id')
    train_service = TrainService()
    exercises=train_service.get_traindayexercises_by_trainday(trainday_id)
    
    return render_template(
        'train/workout.html',
        exercises=exercises,
    )

@train_bp.route('/create-trainplan', methods=['POST'])
@login_required
def create_trainplan():

    name = request.form.get('name')

    if not name:
        flash('El nombre es obligatorio', 'error')
        return redirect(url_for('train.index'))
    
    train_service = TrainService()
    train_service.create_trainplan(current_user.id,name)
    
    return redirect(url_for('train.index'))

@train_bp.route('/delete-trainplan', methods=['POST'])
@login_required
def delete_trainplan():
    
    try:
        trainplan_id = int(request.form.get('trainplan_id'))  
    except (TypeError, ValueError):
        flash('ID de plan inválido', 'error')
        return redirect(url_for('train.index'))

    if not trainplan_id:
        flash('Training plan not found', 'error')
        return redirect(url_for('train.index'))
    
    train_service=TrainService()
    train_service.delete_trainplan(trainplan_id)

    return redirect(url_for('train.index'))

@train_bp.route('/delete-trainday', methods=['POST'])
@login_required
def delete_trainday():
    try:
        print("=== DELETE TRAINDAY ===")
        print(f"Form data: {request.form}")
        
        trainplan_id = int(request.form.get('trainplan_id'))
        trainday_id = int(request.form.get('trainday_id'))
        
        print(f"trainplan_id: {trainplan_id} (tipo: {type(trainplan_id)})")
        print(f"trainday_id: {trainday_id} (tipo: {type(trainday_id)})")
        
    except (TypeError, ValueError) as e:
        print(f"ERROR de conversión: {e}")
        flash('ID inválido', 'error')
        return redirect(url_for('train.index'))
    
    train_service = TrainService()
    result = train_service.delete_trainday(trainday_id)
    
    print(f"Resultado del servicio: {result}")
    
    if result.get('success'):
        print("Eliminación exitosa")
        flash('Training day eliminado correctamente', 'success')
    else:
        print(f"Error en eliminación: {result.get('error')}")
        flash(f'Error: {result.get("error")}', 'error')
    
    return get_traindays(trainplan_id)

@train_bp.route('/delete-traindayexercise', methods=['POST'])
@login_required
def delete_traindayexercise():
    try:

        
        trainplan_id = int(request.form.get('trainplan_id'))
        traindayexercise_id = int(request.form.get('traindayexercise_id'))
        
        
    except (TypeError, ValueError) as e:
        print(f"ERROR de conversión: {e}")
        flash('ID inválido', 'error')
        return redirect(url_for('train.index'))
    
    train_service = TrainService()
    result = train_service.delete_traindayexercise(traindayexercise_id)
    
    print(f"Resultado del servicio: {result}")
    
    if result.get('success'):
        print("Eliminación exitosa")

    else:
        print(f"Error en eliminación: {result.get('error')}")
        flash(f'Error: {result.get("error")}', 'error')
    
    return get_traindays(trainplan_id)

@train_bp.route('/update-trainplan', methods=['POST'])
@login_required
def update_trainplan():
    
    try:
        
        trainplan_id = request.form.get('trainplan_id')
        name = request.form.get('name')
    except (TypeError, ValueError):
        flash('ID de plan inválido', 'error')
        return redirect(url_for('train.index'))

    if not trainplan_id:
        flash('Training plan not found', 'error')
        return redirect(url_for('train.index'))
    
    train_service=TrainService()
    train_service.update_traindayplan(trainplan_id,name)
    return redirect(url_for('train.index'))

@train_bp.route('/update-trainday', methods=['POST'])
@login_required
def update_trainday():
    
    try:
        trainday_id = request.form.get('trainday_id')
        name = request.form.get('name')

    except (TypeError, ValueError):
        flash('ID de plan inválido', 'error')
        return redirect(url_for('train.index'))

    train_service=TrainService()
    trainday=train_service.get_trainday_by_id(trainday_id)
    trainplan_id=trainday["Trainplan_idTrainplan"]
    train_service.update_trainday(trainday_id,name)
    

    return get_traindays(trainplan_id)


@train_bp.route('/get-traindays-html/<int:trainplan_id>')
@login_required
def get_traindays(trainplan_id):
    train_service = TrainService()
    traindays = train_service.get_traindays_by_trainplan(trainplan_id)
    traindayexercises = []
    exercises = train_service.get_exercises()

    for td in traindays:
        ejercicios_td = train_service.get_traindayexercises_by_trainday(td['idTrainday'])
        traindayexercises.extend(ejercicios_td)
    
    # Calcular total de series por grupo muscular
    musclegroup_totals = {}
    for tde in traindayexercises:
        musclegroup = tde['musclegroup']
        numSets = tde['numSets']
        musclegroup_totals[musclegroup] = musclegroup_totals.get(musclegroup, 0) + numSets
    
    # Renderizar el template parcial 
    return render_template(
        'train/traindays.html',
        traindays=traindays,
        traindayexercises=traindayexercises,
        trainplan_id=trainplan_id,
        exercises=exercises,
        musclegroup_totals=musclegroup_totals 
    )

@train_bp.route('/create-trainday', methods=['POST'])
@login_required
def create_trainday():
    name = request.form.get('name')
    trainplan_id = request.form.get('trainplan_id')
    
    # Validar que ambos campos existan
    if not name:
        flash('El nombre es obligatorio', 'error')
        return redirect(url_for('train.index'))
    
    if not trainplan_id:
        flash('El ID del plan es obligatorio', 'error')
        return redirect(url_for('train.index'))
    
    train_service = TrainService()
    result = train_service.create_trainday(current_user.id, name, trainplan_id)
    
    # Verificar el resultado de la operación
    if result and result.get('success'):
        flash('Día de entrenamiento creado exitosamente', 'success')
    else:
        error_msg = result.get('error', 'Error desconocido') if result else 'Error al crear el día de entrenamiento'
        flash(f'Error al crear el día de entrenamiento: {error_msg}', 'error')
    
    # Redirigir a la página principal
    return get_traindays(trainplan_id)

@train_bp.route('/create-traindayexercise', methods=['POST'])
@login_required
def create_traindayexercise():

    numSets = request.form.get('numSets')
    exercise_id = request.form.get('exercise_id')
    trainday_id = request.form.get('trainday_id')
    trainplan_id = request.form.get('trainplan_id')
    notes=request.form.get('notes')
    
    train_service = TrainService()
    train_service.create_trainday_exercise(numSets,exercise_id,trainday_id,trainplan_id,current_user.id,notes)
    
    # Redirigir a la página principal
    return get_traindays(trainplan_id)

@train_bp.route('/move-traindayexercise/<int:traindayexercise_id>/<string:direction>/<int:trainplan_id>', methods=['POST'])
@login_required
def move_traindayexercise(traindayexercise_id, direction, trainplan_id):
    train_service = TrainService()
    result = train_service.move_traindayexercise(traindayexercise_id, direction)
    
    if result.get('success'):
        return get_traindays(trainplan_id)
    else:
        flash(f'Error: {result.get("error")}', 'error')
        return get_traindays(trainplan_id)
    
@train_bp.route('/save-workout', methods=['POST'])
@login_required
def save_workout():
    """Guardar los datos del workout completado"""
    
    # Obtener todos los exercise_ids del formulario
    exercise_ids = request.form.getlist('exercise_ids')
    
    # Diccionario para almacenar los datos procesados
    workout_data = []
    
    # Procesar cada ejercicio
    for exercise_id in exercise_ids:
        exercise_id = int(exercise_id)
        
        # Encontrar todas las series para este ejercicio
        # Buscamos campos que empiecen con "reps_{exercise_id}_"
        prefix = f"reps_{exercise_id}_"
        set_indices = []
        
        for key in request.form.keys():
            if key.startswith(prefix):
                # Extraer el índice de la serie
                set_index = int(key.split('_')[-1])
                set_indices.append(set_index)
        
        # Ordenar los índices
        set_indices.sort()
        
        # Procesar cada serie
        for set_index in set_indices:
            reps_key = f"reps_{exercise_id}_{set_index}"
            weight_key = f"weight_{exercise_id}_{set_index}"
            
            reps = request.form.get(reps_key)
            weight = request.form.get(weight_key)
            
            # Solo guardar si ambos campos están presentes
            if reps and weight:
                workout_data.append({
                    'exercise_id': exercise_id,
                    'reps': int(reps),
                    'weight': float(weight),
                    'date': datetime.now()
                })
    
    # Guardar en la base de datos usando el servicio
    train_service = TrainService()
    result = train_service.save_workout(workout_data, current_user.id)
    
    if result.get('success'):
        flash('Workout guardado exitosamente!', 'success')
        return redirect(url_for('train.index'))
    else:
        flash(f'Error al guardar el workout: {result.get("error")}', 'error')
        return redirect(url_for('train.index'))    
    
@train_bp.route('/keep-alive')
def keep_alive():
    """Endpoint para mantener activa la BD de Aiven y el servicio de Render"""
    try:
        train_service = TrainService()
        exercises = train_service.get_exercises()
        return {
            "status": "ok",
            "exercises_count": len(exercises),
            "timestamp": datetime.now().isoformat()
        }, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500    
