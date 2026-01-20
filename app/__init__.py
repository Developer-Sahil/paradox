from flask import Flask
from firebase_utils import get_firestore_client
from config import config

db = None

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize Firebase
    global db
    db = get_firestore_client()
    
    # Register blueprints
    from app.routes import main, writings, products, projects, systems, vault, arena, metrics, work, admin
    
    app.register_blueprint(main.bp)
    app.register_blueprint(writings.bp, url_prefix='/writings')
    app.register_blueprint(products.bp, url_prefix='/products')
    app.register_blueprint(projects.bp, url_prefix='/projects')
    app.register_blueprint(systems.bp, url_prefix='/systems')
    app.register_blueprint(vault.bp, url_prefix='/vault')
    app.register_blueprint(arena.bp, url_prefix='/arena')
    app.register_blueprint(metrics.bp, url_prefix='/metrics')
    app.register_blueprint(work.bp, url_prefix='/work')
    app.register_blueprint(admin.bp, url_prefix='/admin')
    
    return app