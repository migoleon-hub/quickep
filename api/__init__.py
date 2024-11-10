# api/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import config

db = SQLAlchemy()

def create_app(config_name='production'):  # Changed default to production
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    with app.app_context():
        # Register blueprints
        try:
            from api.routes import main_bp, auth_bp
            app.register_blueprint(main_bp)
            app.register_blueprint(auth_bp)
        except ImportError as e:
            print(f"Error registering main/auth blueprints: {str(e)}")
        
        try:
            from api.routes import documents
            app.register_blueprint(documents.bp)
        except ImportError as e:
            print(f"Error registering documents blueprint: {str(e)}")
            
        # Initialize database
        try:
            db.create_all()
        except Exception as e:
            print(f"Database initialization error: {str(e)}")
            
    return app
