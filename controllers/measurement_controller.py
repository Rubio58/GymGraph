# controllers/measurement_controller.py
from flask import  render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user


measurement_bp = Blueprint('measurement', __name__, url_prefix='/measurement')

@measurement_bp.route('/')
@login_required
def index():
    """Página principal de medidas corporales"""

    
    return render_template(
        'measurement/index.html',

    )