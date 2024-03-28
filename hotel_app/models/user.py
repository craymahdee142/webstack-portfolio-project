from ..extensions import db, bcrypt
from .base_model import BaseModel
from flask_login import UserMixin
from datetime import datetime, timedelta
import secrets
from flask import current_app
from itsdangerous import URLSafeSerializer as Serializer, SignatureExpired, BadSignature
from sqlalchemy_utils import PhoneNumberType


class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(db.String(250), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(PhoneNumberType(), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    image = db.Column(db.String(255), nullable=True)
    
    # Password reset fields
    reset_token = db.Column(db.String(128), nullable=True)
    reset_token_expiration = db.Column(db.DateTime, nullable=True)

    # Password reset generate function
    def generate_reset_token(self):
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expiration = datetime.utcnow() + timedelta(hours=1)
    
    # Check if password reset token is valid
    def is_reset_token_valid(self):
        return self.reset_token_expiration and self.reset_token_expiration > datetime.utcnow()

    # Generte confirmation token
    def generate_confirmation_token(self):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(self.email, salt='email_confirm')

        
    # Confirmation token
    @staticmethod
    def confirm_token(token, expiration=3600):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            email = serializer.loads(token, salt='email_confirm', max_age=expiration)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.filter_by(email=email).first()
        return user
    

    def __init__(self, fullname, username, phone_number, image, email, password, is_admin=False, is_confirmed=False):
        self.fullname = fullname
        self.username = username
        self.phone_number = phone_number
        self.image = image
        self.email = email
        self.is_admin = is_admin
        self.is_confirmed = is_confirmed
        self.set_password(password)
    
    # Password checker
    def set_password(self, password):
        """Create hash password"""
        # bcrypt.hashpw returns a byte string, so we ensure the password is also a byte string
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Check hash password"""
        # We need to encode the password to check and also ensure self.password is in bytes
        return bcrypt.check_password_hash(self.password, password)

    def is_active(self):
        # Check if the account is marked  as active
        return self.is_confirmed
    
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}', is_admin={self.is_admin}>"

