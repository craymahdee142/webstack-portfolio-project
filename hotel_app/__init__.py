from flask import Flask
from config import Config 
from .extensions import db, bcrypt, login_manager, mail, migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from hotel_app.views.roomtype_view import RoomTypeView
from hotel_app.views.rooms_view import RoomView
import os


def create_app(config_class=Config):
    app = Flask(__name__, static_url_path='/static')
    
    UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'upload_folder')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    # Ensure the UPLOAD_FOLDER exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    app.config.from_object(config_class)
    
    # Initialize extensions with the app
    #db = SQLAlchemy()
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    #admin.init_app(app)

    
    login_manager.login_view = 'login'
    login_manager.init_app(app)
        
    # Set up the user loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    admin = Admin(app, name="HotelApp", template_mode='bootstrap4')
    
    # Admin User Model view
  
    #admin.add_view(ModelView(User, db.session, name='user'))
    
    # Models imports
    from hotel_app.models.user import User
    # Modal Views for user
    admin.add_view(ModelView(User, db.session, name='User'))
    
    #from hotel_app.models.rooms import Room
    #admin.add_view(ModelView(Room, db.session, name='Rooms'))
    
    class RoomTypeModelView(ModelView):
        column_list = ('id', 'type_name', 'description', 'base_price', 'max_capaity', 'amenities')
        
    from hotel_app.models.room_type import RoomType
    admin.add_view(RoomTypeModelView(RoomType, db.session, name='RoomTypes'))
    
    class RoomModelView(ModelView):
        column_list = ('id', 'room_number', 'room_status', 'price_per_night', 'amenities', 'additional_note', 'floor_num', 'room_type_id')
        
    class GuestModelView(ModelView):
        column_list = ('id', 'fullname', 'email', 'phone_number', 'mailing_address', 'identify_proof', 'create_at', 'updated_at')
        
        
    from hotel_app.models.rooms import Room
    admin.add_view(RoomModelView(Room, db.session, name='Rooms'))
    
    from hotel_app.models.guest import Guest
    admin.add_view(GuestModelView(Guest, db.session, name='GuestInfo'))
    
    from hotel_app.models.reservation import Reservation
    admin.add_view(ModelView(Reservation, db.session, name='Bookings'))
    

    
    # Base View for posting room types
    admin.add_view(RoomTypeView(name='Posting', endpoint='room_type'))
    
    admin.add_view(RoomView(name='Add-Room', endpoint='rooms'))

    # Import and register blueprints
    
    # Main home page blueprint
    from .views.main_view import main_bp
    app.register_blueprint(main_bp)
    
    # User blueprint
    from .views.user_view import user_bp
    app.register_blueprint(user_bp, url_prefix='/user')
   
    # Utils blueprint
    from .views.utils_view import utils_bp
    app.register_blueprint(utils_bp)
    
    # Guest Blue rpint
    from .views.guest_view import guest_bp
    app.register_blueprint(guest_bp)
   
   # Staff Blue rpint
    from .views.staff_view import staff_bp
    app.register_blueprint(staff_bp)
   
   # Booking Blue rpint
    from .views.booking_view import book_bp
    app.register_blueprint(book_bp)
    
    # Rooms Blue print
    #from .views.rooms_view import rooms_bp
    #app.register_blueprint(rooms_bp)
    
     # Payment Blue print
    from .views.payment_view import payment_bp
    app.register_blueprint(payment_bp)
   
   # Reservation Blue print
    from .views.reservation_view import reserve_bp
    app.register_blueprint(reserve_bp)
    
    # Room Type Blue print
    #from .views.room_type_view import room_type_bp
    #app.register_blueprint(room_type_bp, url_prefix='/admin')
    
    # Review Blue print
    from .views.review_view import review_bp
    app.register_blueprint(review_bp)
   
    # Maintainanace Blue print
    from .views.maintainance_view import maintain_bp
    app.register_blueprint(maintain_bp)
    
    # Service Blue print
    from .views.service_view import service_bp
    app.register_blueprint(service_bp)
    
    # Image Blue print
    from .views.image_view import image_bp
    app.register_blueprint(image_bp)
    
   
    return app
