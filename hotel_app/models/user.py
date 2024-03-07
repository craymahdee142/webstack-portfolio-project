from hotel_app.base_model import BaseModel, db
from flask_login import UserMixin, login_user, current_user
from flask_login import LoginManager, logout_user, login_required
from datetime import datetime, timedelta
import bcrypt
import os


class User(BaseModel, UserMixin):
    __tablename__ = 'users'
    
    fullname = db.Column(db.String(250), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, fullname, username, email, is_admin=False, is_confirmed=False):
        self.fullname = fullname
        self.username = username
        self.email = email
        self.is_admin = is_admin
        self.is_confirmed = is_confirmed
    
    # Password checker
    def set_password(self, password):
        """Create hash password"""
        # bcrypt.hashpw returns a byte string, so we ensure the password is also a byte string
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """Check hash password"""
        # We need to encode the password to check and also ensure self.password is in bytes
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}', is_admin={self.is_admin}>"

