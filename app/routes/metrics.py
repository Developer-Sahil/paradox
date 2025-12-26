from flask import Blueprint, render_template
from firebase_admin import firestore
from app.models.metric import Metric

bp = Blueprint('metrics', __name__)

@bp.route('/')
def index():
    db = firestore.client()
    metrics = Metric.get_all(db)
    
    # Group metrics by category
    grouped = {}
    for metric in metrics:
        cat = metric.category or 'general'
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(metric)
    
    return render_template('metrics.html', grouped_metrics=grouped)