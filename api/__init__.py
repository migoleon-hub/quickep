from flask import Flask
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
    from api.routes import main, auth, documents
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(documents.bp)
    
    return app
