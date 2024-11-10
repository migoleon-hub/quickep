from flask import Blueprint, jsonify

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return jsonify({
        "message": "Welcome to FastKEP API",
        "status": "online",
        "version": "1.0",
        "endpoints": {
            "auth": "/auth",
            "documents": "/documents"
        }
    })
