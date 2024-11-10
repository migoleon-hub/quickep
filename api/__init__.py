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
    
    # Register blueprints
    try:
        from api.routes import main_bp, auth_bp
        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)
    except ImportError as e:
        print(f"Error registering blueprints: {str(e)}")
        pass
        
    # Το documents blueprint θα το προσθέσουμε αργότερα
    # try:
    #     from api.routes import documents
    #     app.register_blueprint(documents.bp)
    # except ImportError:
    #     pass
    
    return app
