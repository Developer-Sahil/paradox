from flask import Blueprint, render_template, abort
from firebase_admin import firestore
from app.models.product import Product

bp = Blueprint('products', __name__)

@bp.route('/')
def index():
    db = firestore.client()
    products = Product.get_all(db, active_only=True)
    return render_template('products/index.html', products=products)

@bp.route('/<slug>')
def detail(slug):
    db = firestore.client()
    product = Product.get_by_slug(db, slug)
    if not product or not product.active:
        abort(404)
    return render_template('products/detail.html', product=product)