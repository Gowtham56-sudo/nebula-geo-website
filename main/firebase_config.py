import os
import json
import logging
import firebase_admin
from firebase_admin import credentials, firestore

logger = logging.getLogger(__name__)

db = None

def initialize_firebase():
    global db
    if db is not None:
        return db

    # Check if already initialized
    try:
        firebase_admin.get_app()
        db = firestore.client()
        return db
    except ValueError:
        pass  # Not initialized yet

    cred = None

    # 1. Try environment variable
    cred_json = os.environ.get('FIREBASE_CREDENTIALS_JSON')
    if cred_json:
        try:
            cred_dict = json.loads(cred_json)
            cred = credentials.Certificate(cred_dict)
            logger.info("Initializing Firebase using FIREBASE_CREDENTIALS_JSON env var.")
        except Exception as e:
            logger.error(f"Failed to load Firebase credentials from env: {e}")

    # 2. Try local file
    if not cred:
        # Check root folder first
        key_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'firebase-key.json')
        if os.path.exists(key_path):
            try:
                cred = credentials.Certificate(key_path)
                logger.info(f"Initializing Firebase using local key: {key_path}")
            except Exception as e:
                logger.error(f"Failed to load Firebase credentials from local file: {e}")
        else:
            logger.warning(f"Firebase key file not found at {key_path}")

    # 3. Initialize
    if cred:
        try:
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            logger.info("Firebase Firestore client initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase app: {e}")
    else:
        logger.error("No Firebase credentials provided. Firebase features will fail.")
    
    return db

# Run initialization on import
initialize_firebase()
