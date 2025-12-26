from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from firebase_admin import firestore, auth
from functools import wraps
from datetime import datetime

bp = Blueprint('admin', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access admin panel', 'error')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id_token = request.form.get('id_token')
        try:
            decoded_token = auth.verify_id_token(id_token)
            session['user'] = {
                'uid': decoded_token['uid'],
                'email': decoded_token.get('email')
            }
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 401
    
    return render_template('admin/login.html')

@bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('admin.login'))

@bp.route('/dashboard')
@login_required
def dashboard():
    db = firestore.client()
    
    writings_count = len(list(db.collection('writings').stream()))
    projects_count = len(list(db.collection('projects').stream()))
    products_count = len(list(db.collection('products').stream()))
    
    return render_template('admin/dashboard.html', 
                         writings_count=writings_count,
                         projects_count=projects_count,
                         products_count=products_count)

# Writings Management
@bp.route('/writings')
@login_required
def writings_list():
    db = firestore.client()
    docs = db.collection('writings').order_by('date', direction=firestore.Query.DESCENDING).stream()
    writings = [{'id': doc.id, **doc.to_dict()} for doc in docs]
    return render_template('admin/writings_list.html', writings=writings)

@bp.route('/writings/new', methods=['GET', 'POST'])
@login_required
def writings_new():
    if request.method == 'POST':
        db = firestore.client()
        title = request.form.get('title')
        data = {
            'title': title,
            'content': request.form.get('content'),
            'date': request.form.get('date') or datetime.utcnow().isoformat(),
            'tags': [t.strip() for t in request.form.get('tags', '').split(',') if t.strip()],
            'series': request.form.get('series') or None,
            'slug': title.lower().replace(' ', '-').replace('/', '-')
        }
        db.collection('writings').add(data)
        flash('Post created successfully', 'success')
        return redirect(url_for('admin.writings_list'))
    
    return render_template('admin/writings_form.html', writing=None)

@bp.route('/writings/<id>/edit', methods=['GET', 'POST'])
@login_required
def writings_edit(id):
    db = firestore.client()
    doc_ref = db.collection('writings').document(id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        data = {
            'title': title,
            'content': request.form.get('content'),
            'date': request.form.get('date'),
            'tags': [t.strip() for t in request.form.get('tags', '').split(',') if t.strip()],
            'series': request.form.get('series') or None,
            'slug': title.lower().replace(' ', '-').replace('/', '-')
        }
        doc_ref.update(data)
        flash('Post updated successfully', 'success')
        return redirect(url_for('admin.writings_list'))
    
    doc = doc_ref.get()
    writing = {'id': doc.id, **doc.to_dict()} if doc.exists else None
    return render_template('admin/writings_form.html', writing=writing)

@bp.route('/writings/<id>/delete', methods=['POST'])
@login_required
def writings_delete(id):
    db = firestore.client()
    db.collection('writings').document(id).delete()
    flash('Post deleted successfully', 'success')
    return redirect(url_for('admin.writings_list'))

# Projects Management
@bp.route('/projects')
@login_required
def projects_list():
    db = firestore.client()
    docs = db.collection('projects').stream()
    projects = [{'id': doc.id, **doc.to_dict()} for doc in docs]
    return render_template('admin/projects_list.html', projects=projects)

@bp.route('/projects/new', methods=['GET', 'POST'])
@login_required
def projects_new():
    if request.method == 'POST':
        db = firestore.client()
        title = request.form.get('title')
        data = {
            'title': title,
            'description': request.form.get('description'),
            'demo_url': request.form.get('demo_url') or None,
            'github_url': request.form.get('github_url') or None,
            'tech_stack': [t.strip() for t in request.form.get('tech_stack', '').split(',') if t.strip()],
            'status': request.form.get('status', 'active'),
            'slug': title.lower().replace(' ', '-').replace('/', '-')
        }
        db.collection('projects').add(data)
        flash('Project created successfully', 'success')
        return redirect(url_for('admin.projects_list'))
    
    return render_template('admin/projects_form.html', project=None)

@bp.route('/projects/<id>/edit', methods=['GET', 'POST'])
@login_required
def projects_edit(id):
    db = firestore.client()
    doc_ref = db.collection('projects').document(id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        data = {
            'title': title,
            'description': request.form.get('description'),
            'demo_url': request.form.get('demo_url') or None,
            'github_url': request.form.get('github_url') or None,
            'tech_stack': [t.strip() for t in request.form.get('tech_stack', '').split(',') if t.strip()],
            'status': request.form.get('status', 'active'),
            'slug': title.lower().replace(' ', '-').replace('/', '-')
        }
        doc_ref.update(data)
        flash('Project updated successfully', 'success')
        return redirect(url_for('admin.projects_list'))
    
    doc = doc_ref.get()
    project = {'id': doc.id, **doc.to_dict()} if doc.exists else None
    return render_template('admin/projects_form.html', project=project)

@bp.route('/projects/<id>/delete', methods=['POST'])
@login_required
def projects_delete(id):
    db = firestore.client()
    db.collection('projects').document(id).delete()
    flash('Project deleted successfully', 'success')
    return redirect(url_for('admin.projects_list'))

# Products Management
@bp.route('/products')
@login_required
def products_list():
    db = firestore.client()
    docs = db.collection('products').stream()
    products = [{'id': doc.id, **doc.to_dict()} for doc in docs]
    return render_template('admin/products_list.html', products=products)

@bp.route('/products/new', methods=['GET', 'POST'])
@login_required
def products_new():
    if request.method == 'POST':
        db = firestore.client()
        title = request.form.get('title')
        data = {
            'title': title,
            'description': request.form.get('description'),
            'price': float(request.form.get('price', 0)),
            'url': request.form.get('url') or None,
            'active': request.form.get('active') == 'on',
            'slug': title.lower().replace(' ', '-').replace('/', '-')
        }
        db.collection('products').add(data)
        flash('Product created successfully', 'success')
        return redirect(url_for('admin.products_list'))
    
    return render_template('admin/products_form.html', product=None)

@bp.route('/products/<id>/edit', methods=['GET', 'POST'])
@login_required
def products_edit(id):
    db = firestore.client()
    doc_ref = db.collection('products').document(id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        data = {
            'title': title,
            'description': request.form.get('description'),
            'price': float(request.form.get('price', 0)),
            'url': request.form.get('url') or None,
            'active': request.form.get('active') == 'on',
            'slug': title.lower().replace(' ', '-').replace('/', '-')
        }
        doc_ref.update(data)
        flash('Product updated successfully', 'success')
        return redirect(url_for('admin.products_list'))
    
    doc = doc_ref.get()
    product = {'id': doc.id, **doc.to_dict()} if doc.exists else None
    return render_template('admin/products_form.html', product=product)

@bp.route('/products/<id>/delete', methods=['POST'])
@login_required
def products_delete(id):
    db = firestore.client()
    db.collection('products').document(id).delete()
    flash('Product deleted successfully', 'success')
    return redirect(url_for('admin.products_list'))