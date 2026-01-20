import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
import logging

logger = logging.getLogger(__name__)

def initialize_firebase():
    """
    Initialize Firebase Admin SDK with proper credential handling.
    Supports multiple credential sources in order of preference:
    1. GOOGLE_APPLICATION_CREDENTIALS environment variable (file path)
    2. FIREBASE_CREDENTIALS environment variable (JSON string)
    3. Application Default Credentials (for GCP environments)
    """
    if firebase_admin._apps:
        logger.info("Firebase already initialized")
        return firebase_admin.get_app()

    # Method 1: File path from environment variable
    cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if cred_path and os.path.exists(cred_path):
        logger.info(f"Initializing Firebase with credentials file: {cred_path}")
        cred = credentials.Certificate(cred_path)
    else:
        # Method 2: JSON string from environment variable
        cred_json = os.getenv('FIREBASE_CREDENTIALS')
        if cred_json:
            logger.info("Initializing Firebase with credentials from environment variable")
            try:
                cred_dict = json.loads(cred_json)
                cred = credentials.Certificate(cred_dict)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in FIREBASE_CREDENTIALS: {e}")
                raise
        else:
            # Method 3: Application Default Credentials
            logger.info("Initializing Firebase with Application Default Credentials")
            cred = credentials.ApplicationDefault()

    # Get database URL
    database_url = os.getenv('FIREBASE_DATABASE_URL')
    if not database_url:
        logger.warning("FIREBASE_DATABASE_URL not set, using default Firestore instance")

    # Initialize the app
    app = firebase_admin.initialize_app(cred, {
        'databaseURL': database_url
    } if database_url else {})

    logger.info("Firebase initialized successfully")
    return app

def get_firestore_client():
    """Get Firestore client, initializing Firebase if necessary."""
    initialize_firebase()
    return firestore.client()