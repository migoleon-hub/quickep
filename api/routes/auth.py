# api/routes/auth.py
from flask import Blueprint, request, jsonify, current_app
from api.models import User, TokenBlocklist
from api import db
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import re

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Setup rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["5 per minute", "100 per hour"]
)

def validate_password(password):
    """Validate password against policy"""
    if len(password) < current_app.config['PASSWORD_MIN_LENGTH']:
        return False, "Password must be at least 8 characters long"
        
    if current_app.config['PASSWORD_REQUIRE_UPPER'] and not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
        
    if current_app.config['PASSWORD_REQUIRE_LOWER'] and not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
        
    if current_app.config['PASSWORD_REQUIRE_DIGITS'] and not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
        
    if current_app.config['PASSWORD_REQUIRE_SPECIAL'] and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
        
    return True, None

def create_tokens(user_id):
    """Create access and refresh tokens"""
    access_token = jwt.encode({
        'user_id': user_id,
        'type': 'access',
        'exp': datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
    }, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
    
    refresh_token = jwt.encode({
        'user_id': user_id,
        'type': 'refresh',
        'exp': datetime.utcnow() + current_app.config['JWT_REFRESH_TOKEN_EXPIRES']
    }, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
    
    return access_token, refresh_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
            
        try:
            # Check if token is blacklisted
            if TokenBlocklist.is_blacklisted(token):
                raise jwt.InvalidTokenError('Token is blacklisted')
                
            data = jwt.decode(
                token, 
                current_app.config['JWT_SECRET_KEY'], 
                algorithms=['HS256']
            )
            
            if data['type'] != 'access':
                raise jwt.InvalidTokenError('Invalid token type')
                
            current_user = User.query.get(data['user_id'])
            if not current_user:
                raise jwt.InvalidTokenError('User not found')
                
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({'message': str(e)}), 401
            
        return f(current_user, *args, **kwargs)
    return decorated

@bp.route('/register', methods=['POST'])
@limiter.limit("3/minute")  # Limit registration attempts
def register():
    data = request.get_json()
    
    # Validate required fields
    if not all(k in data for k in ['email', 'password']):
        return jsonify({'message': 'Missing required fields'}), 400
        
    # Validate password
    is_valid, error_message = validate_password(data['password'])
    if not is_valid:
        return jsonify({'message': error_message}), 400
        
    # Check if user exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 409
        
    # Create user
    user = User(
        email=data['email'],
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', '')
    )
    user.password = data['password']
    
    db.session.add(user)
    db.session.commit()
    
    # Generate tokens
    access_token, refresh_token = create_tokens(user.id)
    
    return jsonify({
        'message': 'User created successfully',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 201

@bp.route('/login', methods=['POST'])
@limiter.limit("5/minute")  # Limit login attempts
def login():
    data = request.get_json()
    
    if not all(k in data for k in ['email', 'password']):
        return jsonify({'message': 'Missing credentials'}), 400
        
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.verify_password(data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
        
    access_token, refresh_token = create_tokens(user.id)
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    })

@bp.route('/refresh', methods=['POST'])
def refresh():
    refresh_token = request.json.get('refresh_token')
    
    if not refresh_token:
        return jsonify({'message': 'Refresh token is missing'}), 400
        
    try:
        data = jwt.decode(
            refresh_token, 
            current_app.config['JWT_SECRET_KEY'], 
            algorithms=['HS256']
        )
        
        if data['type'] != 'refresh':
            raise jwt.InvalidTokenError('Invalid token type')
            
        # Check if token is blacklisted
        if TokenBlocklist.is_blacklisted(refresh_token):
            raise jwt.InvalidTokenError('Token is blacklisted')
            
        # Generate new access token
        access_token = jwt.encode({
            'user_id': data['user_id'],
            'type': 'access',
            'exp': datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
        }, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
        
        return jsonify({'access_token': access_token})
        
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Refresh token has expired'}), 401
    except jwt.InvalidTokenError as e:
        return jsonify({'message': str(e)}), 401

@bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    token = request.headers.get('Authorization').split(' ')[1]
    
    # Add token to blacklist
    TokenBlocklist.add(token)
    
    return jsonify({'message': 'Successfully logged out'})

@bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    return jsonify(current_user.to_dict())
