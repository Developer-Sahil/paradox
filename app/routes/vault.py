from flask import Blueprint, render_template, abort, request
from firebase_admin import firestore
import markdown

bp = Blueprint('vault', __name__)

@bp.route('/')
def index():
    db = firestore.client()
    category = request.args.get('category')
    
    vault_ref = db.collection('vault')
    if category:
        docs = vault_ref.where('category', '==', category).stream()
    else:
        docs = vault_ref.stream()
    
    items = []
    categories = set()
    for doc in docs:
        data = doc.to_dict()
        data['id'] = doc.id
        items.append(data)
        if data.get('category'):
            categories.add(data['category'])
    
    return render_template('vault/index.html', items=items, categories=sorted(categories), current_category=category)

@bp.route('/<item_id>')
def detail(item_id):
    db = firestore.client()
    doc = db.collection('vault').document(item_id).get()
    if not doc.exists:
        abort(404)
    
    item = doc.to_dict()
    item['id'] = doc.id
    item['html_content'] = markdown.markdown(item.get('content', ''), extensions=['fenced_code', 'codehilite'])
    
    return render_template('vault/detail.html', item=item)