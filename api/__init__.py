from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints σταδιακά
    try:
        from api.routes import main
        app.register_blueprint(main.bp)
    except ImportError:
        pass
        
    # Τα υπόλοιπα blueprints θα τα ενεργοποιήσουμε
    # μόλις έχουμε όλα τα απαραίτητα models και dependencies
    # try:
    #     from api.routes import auth, documents
    #     app.register_blueprint(auth.bp)
    #     app.register_blueprint(documents.bp)
    # except ImportError:
    #     pass
    
    return app
