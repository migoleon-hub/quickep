from flask import Blueprint, request, jsonify, current_app
from api.models import User
from api import db
import jwt
from datetime import datetime, timedelta
from functools import wraps

bp = Blueprint('auth', __name__, url_prefix='/auth')

def create_token(user_id):
    """Δημιουργεί ένα JWT token για τον χρήστη"""
    return jwt.encode({
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1)  # Token διάρκειας 24 ωρών
    }, current_app.config['SECRET_KEY'], algorithm='HS256')

def token_required(f):
    """Decorator για να προστατεύουμε τα endpoints που απαιτούν authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
            
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401
            
        return f(current_user, *args, **kwargs)
    return decorated

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Έλεγχος required fields
    if not all(k in data for k in ['email', 'password']):
        return jsonify({'message': 'Missing required fields'}), 400
        
    # Έλεγχος αν υπάρχει ήδη ο χρήστης
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 409
        
    # Δημιουργία νέου χρήστη
    user = User(
        email=data['email'],
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', '')
    )
    user.password = data['password']  # Χρησιμοποιεί το password setter για κρυπτογράφηση
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User created successfully',
        'user': user.to_dict()
    }), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not all(k in data for k in ['email', 'password']):
        return jsonify({'message': 'Missing credentials'}), 400
        
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.verify_password(data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
        
    token = create_token(user.id)
    
    return jsonify({
        'token': token,
        'user': user.to_dict()
    })

@bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    return jsonify(current_user.to_dict())
