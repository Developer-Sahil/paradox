from flask import Blueprint, render_template
from firebase_admin import firestore

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/operator')
def operator():
    return render_template('operator.html')