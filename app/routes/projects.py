from flask import Blueprint, render_template, abort
from firebase_admin import firestore
from app.models.project import Project

bp = Blueprint('projects', __name__)

@bp.route('/')
def index():
    db = firestore.client()
    projects = Project.get_all(db, status='active')
    return render_template('projects/index.html', projects=projects)

@bp.route('/<slug>')
def detail(slug):
    db = firestore.client()
    project = Project.get_by_slug(db, slug)
    if not project:
        abort(404)
    return render_template('projects/detail.html', project=project)