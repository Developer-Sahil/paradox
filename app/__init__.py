from flask import Flask
import firebase_admin
from firebase_admin import credentials, firestore
import json
import os
from config import config

db = None

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize Firebase
    global db
    if not firebase_admin._apps:
        # Try to get credentials from file path first
        cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if cred_path and os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
        else:
            # Fall back to JSON string from env
            cred_json = app.config.get('FIREBASE_CREDENTIALS')
            if cred_json:
                cred_dict = json.loads(cred_json)
                cred = credentials.Certificate(cred_dict)
            else:
                cred = credentials.ApplicationDefault()
        
        firebase_admin.initialize_app(cred, {
            'databaseURL': app.config.get('FIREBASE_DATABASE_URL')
        })
    
    db = firestore.client()
    
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