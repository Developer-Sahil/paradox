from flask import Blueprint, render_template

bp = Blueprint('work', __name__)

@bp.route('/')
def index():
    return render_template('work.html')