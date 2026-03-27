# controllers/measurement_controller.py
from flask import  render_template, Blueprint
from flask_login import login_required
from services.train_service import TrainService

progress_bp = Blueprint('progress', __name__, url_prefix='/progress')

@progress_bp.route('/')
@login_required
def index():
    """Página principal de progreso"""
    train_service = TrainService()
    exercises = train_service.get_exercises()

    return render_template(
        'progress/index.html',
        exercises=exercises
    )

@progress_bp.route('/get-sets-html/<int:exercise_id>')
@login_required
def get_sets(exercise_id):
    train_service = TrainService()
    sets= train_service.get_sets_by_exercise(exercise_id)
   
    # Renderizar el template parcial 
    return render_template(
        'progress/sets.html',
        sets=sets
    )