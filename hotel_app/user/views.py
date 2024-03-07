
from flask import Blueprint, url_for, request, redirect, render_template, flash, jsonify
from ..base_model import db
from hotel_app.models import User
from flask_login import current_user, login_user, logout_user 
from ..extensions import bcrypt, login_manager
import re

user_bp = Blueprint('user_bp', __name__)


# Validate email address
def is_valid_email(email):
    pattern = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
    return re.match(pattern, email, re.I)

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

        # Hash the password
        hash_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Check if username is already taken
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists", "error")
            return redirect(url_for("user_bp.register"))
        
        # Create new user instance
        new_user = User(fullname=fullname, username=username, email=email)
        new_user.set_password(hash_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful", 'success')
            #redirect(url_for(user_bp.login))
        except Exception as e:
            flash("An error occured. Please try again.", 'error ')
            db.session.rollback()
            return redirect(url_for("user_bp.register"))
        return redirect(url_for(user_bp.login))

    return render_template("register.html")

        
@user_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("You have successfully logged in", 'success')
            return redirect(url_for("home_bp.home"))

        else:
            flash("Invalid email or password", 'danger')
    return render_template("login.html")
        

@user_bp.route("/logout")
def logout():
    login_user()
    flash("You have successful logged out", 'info')
    return redirect(url_for("home.html"))
