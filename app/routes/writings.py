from flask import Blueprint, render_template, abort
from firebase_admin import firestore
from app.models.post import Post
import markdown

bp = Blueprint('writings', __name__)

@bp.route('/')
def index():
    db = firestore.client()
    posts = Post.get_all(db)
    return render_template('writings/index.html', posts=posts)

@bp.route('/<slug>')
def detail(slug):
    db = firestore.client()
    post = Post.get_by_slug(db, slug)
    if not post:
        abort(404)
    
    # Convert markdown to HTML
    post.html_content = markdown.markdown(post.content, extensions=['fenced_code', 'codehilite'])
    
    return render_template('writings/detail.html', post=post)

@bp.route('/series/<series_name>')
def series(series_name):
    db = firestore.client()
    posts = Post.get_by_series(db, series_name)
    return render_template('writings/series.html', posts=posts, series=series_name)