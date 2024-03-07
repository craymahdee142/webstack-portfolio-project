from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
from config import Config 
from .extensions import db, bcrypt, login_manager, migrate
from .models import User
#from .base_model import BaseModel

#db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app)
    
    login_manager.login_view = 'login'
    login_manager.init_app(app)
    

    with app.app_context():
        db.create_all()
        
        
    # Set up the user loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Import and register blueprints
    from hotel_app.user import user_bp
    app.register_blueprint(user_bp)

    from hotel_app.home import home_bp
    app.register_blueprint(home_bp)
    

    return app
