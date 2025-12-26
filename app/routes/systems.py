from flask import Blueprint, render_template, abort
from firebase_admin import firestore

bp = Blueprint('systems', __name__)

@bp.route('/')
def index():
    db = firestore.client()
    tools = []
    docs = db.collection('tools').stream()
    for doc in docs:
        data = doc.to_dict()
        data['id'] = doc.id
        tools.append(data)
    return render_template('systems/index.html', tools=tools)

@bp.route('/<tool_id>')
def detail(tool_id):
    db = firestore.client()
    doc = db.collection('tools').document(tool_id).get()
    if not doc.exists:
        abort(404)
    tool = doc.to_dict()
    tool['id'] = doc.id
    return render_template('systems/detail.html', tool=tool)