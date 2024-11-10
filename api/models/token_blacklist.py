# api/models/token_blacklist.py
from api import db
from datetime import datetime

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    @classmethod
    def add(cls, token):
        """Add a token to the blacklist"""
        try:
            decoded_token = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            jti = decoded_token['jti']
            token_blacklist = cls(jti=jti)
            db.session.add(token_blacklist)
            db.session.commit()
            return True
        except:
            return False
    
    @classmethod
    def is_blacklisted(cls, token):
        """Check if a token is blacklisted"""
        try:
            decoded_token = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            jti = decoded_token['jti']
            return cls.query.filter_by(jti=jti).first() is not None
        except:
            return True
