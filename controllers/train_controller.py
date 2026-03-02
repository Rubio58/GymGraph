# controllers/train_controller.py
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
        trainplan_id = int(request.form.get('trainplan_id'))  # Convertir aquí
    except (TypeError, ValueError):
        flash('ID de plan inválido', 'error')
        return redirect(url_for('train.index'))

    if not trainplan_id:
        flash('Training plan not found', 'error')
        return redirect(url_for('train.index'))
    
    train_service=TrainService()
    train_service.delete_trainplan(trainplan_id)

    return redirect(url_for('train.index'))


@train_bp.route('/get-traindays-html/<int:trainplan_id>')
@login_required
def get_traindays(trainplan_id):
    train_service = TrainService()
    traindays = train_service.get_traindays_by_trainplan(trainplan_id)
    traindayexercises = []
    exercises = train_service.get_exercises()

    for td in traindays:
        ejercicios_td = train_service.get_traindayexercises_by_trainday(td['idTrainday'])
        traindayexercises.extend(ejercicios_td)  # Se usa extend en lugar de append para que sea una lista plana y no una lista de listas
    
    # Renderizar un template parcial que contiene los traindays
    return render_template(
        'train/traindays.html',
        traindays=traindays,
        traindayexercises=traindayexercises,
        trainplan_id=trainplan_id,
        exercises=exercises
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
