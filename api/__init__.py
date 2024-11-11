from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import config

db = SQLAlchemy()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per hour"],
    storage_uri="memory://"
)

def create_app(config_name='production'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    limiter.init_app(app)
    
    with app.app_context():
        # Register blueprints
        from api.routes import main_bp, auth_bp
        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)
        
        # Initialize database
        db.create_all()
            
    return app
    
def register_error_handlers(app):
    @app.errorhandler(500)
    def handle_500(error):
        app.logger.error(f'Server error: {error}')
        return jsonify({
            'error': 'Internal server error',
            'message': str(error)
        }), 500

    @app.errorhandler(503)
    def handle_503(error):
        app.logger.error(f'Service unavailable: {error}')
        return jsonify({
            'error': 'Service temporarily unavailable',
            'message': 'The server is currently unable to handle the request'
        }), 503

    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.error(f'Unhandled exception: {error}')
        return jsonify({
            'error': 'Unexpected error',
            'message': str(error)
        }), 500
