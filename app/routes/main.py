from flask import Blueprint, render_template
from firebase_admin import firestore
from app.models.post import Post

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    # Fetch latest 3 writings from Firestore
    db = firestore.client()
    latest_posts = Post.get_all(db)[:3]  # Get first 3 posts (already ordered by date desc)
    
    return render_template('home.html', latest_posts=latest_posts)

@bp.route('/operator')
def operator():
    return render_template('operator.html')