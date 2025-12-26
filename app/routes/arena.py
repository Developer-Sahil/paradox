from flask import Blueprint, render_template, abort
from firebase_admin import firestore
import markdown

bp = Blueprint('arena', __name__)

@bp.route('/')
def index():
    db = firestore.client()
    docs = db.collection('arena').order_by('date', direction=firestore.Query.DESCENDING).stream()
    
    posts = []
    for doc in docs:
        data = doc.to_dict()
        data['id'] = doc.id
        posts.append(data)
    
    return render_template('arena/index.html', posts=posts)

@bp.route('/<post_id>')
def detail(post_id):
    db = firestore.client()
    doc = db.collection('arena').document(post_id).get()
    if not doc.exists:
        abort(404)
    
    post = doc.to_dict()
    post['id'] = doc.id
    post['html_content'] = markdown.markdown(post.get('content', ''), extensions=['fenced_code', 'codehilite'])
    
    return render_template('arena/detail.html', post=post)