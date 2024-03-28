from flask import Blueprint, render_template, redirect, request, url_for, flash, current_app
from ..models.user import User
from ..models.guest import Guest
from ..extensions import db, bcrypt
from flask_login import login_user, logout_user
from .utils_view import send_confirmation_email
from sqlalchemy import or_ # For handling more queries
from flask import session
import re


user_bp = Blueprint('user_bp', __name__)

# Validate email address
def is_valid_email(email):
    pattern = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
    return re.match(pattern, email, re.I)


# Email confirmation
@user_bp.route("/user/confirm_email/<token>")
def confirm_email(token):
    user = User.confirm_token(token)
    
    if user:
        user.is_confirmed = True
        db.session.commit()
        flash("Your email has been confirmed!", 'success')
        return redirect(url_for('main_bp.home'))
    else:
        flash("The confirmation link is invalid or has expired.", "error")
        return redirect(url_for('main_bp.register'))
    


@user_bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        if not is_valid_email(email):
            flash("Invalid email address", 'error')
            return redirect(url_for('user_bp.register'))
        
        # Extract data from submission form
        fullname = request.form.get('fullname')
        username = request.form.get('username')
        phone_number = request.form.get('phone_number') 
        email = request.form.get('email')
        password = request.form.get('password')
        confirmed_password = request.form.get('confirmed_password')
        
        # Check if password is empty
        if not password:
            flash("Password cannot be empty", "error")
            return redirect(url_for("user_bp.register"))
                
        # Check if password and password verify match
        if password != confirmed_password:
            flash("Passwords do not match", "error")
            return redirect(url_for("user_bp.register"))

        # Check if username  email is already taken
        existing_user = User.query.filter(User.username == username, User.email == email).first()
        if existing_user:
            flash("Username or email already exists", "error")
            return redirect(url_for("user_bp.register"))
        
        # Hash the password
        hash_password = bcrypt.generate_password_hash(password).decode("utf-8")

          # Create new user instance
        user = User(fullname=fullname, username=username, phone_number=phone_number, email=email, password=password)
        user.set_password(password)
        
        guest = Guest(
            fullname=fullname,
            email=email,
            phone_number=phone_number
        )
        
        db.session.add(user)
        db.session.add(guest)
        db.session.commit()
        try:  
            # Send email confirmation
            send_confirmation_email(user.email, user)
            
            flash("Please check your email to confirm your account", 'success')
            return redirect(url_for('main_bp.login'))
        except Exception as e:
            flash("An error occured. Please try again.", 'error ')
            print(f"Failed to send confirmation email: {e}")

            db.session.rollback()
            return redirect(url_for("user_bp.register"))

    return render_template("register.html")

# Login blueprint route
@user_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        current_app.logger.info(f"Attempting login for email: {email}")

        if user and bcrypt.check_password_hash(user.password, password):
            # Check if user email account is confirmed
            if user.is_confirmed:
                login_user(user)
                current_app.logger.info("Login successful")

                # Find corresponding guest using email
                guest = Guest.query.filter_by(email=email).first()
                if guest:
                    # Store guest_id in session if corresponding guest is found
                    session['guest_id'] = guest.id
                
                flash("You have successfully logged in", 'success')
                return redirect(url_for("main_bp.home"))
            else:
                # User's email is not confirmed
                flash("Kindly confirm your email account before logging in!", 'warning')
                return redirect(url_for('user_bp.login'))

        else:
            flash("Invalid email or password", 'error')
            current_app.logger.warning(f"Failed login attempt for {email}")

    return render_template("login.html")
        
# Logout route
@user_bp.route("/logout")
def logout():
    logout_user()
    session.pop('guest_id', None)
    flash("You have successful logged out", 'info')
    return redirect(url_for("main_bp.home"))