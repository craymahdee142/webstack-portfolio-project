from flask import Blueprint, render_template


main_bp = Blueprint('main_bp', __name__)

# Main home route
@main_bp.route("/")
def home():
    return render_template("index.html")

# About us route

@main_bp.route("/about")
def about():
    return render_template("about.html")

# Contact us route
@main_bp.route("/contact")
def contact():
    return render_template("contact.html") 

# Login route
@main_bp.route("/login")
def login():
    return render_template("login.html") 

# Register route
@main_bp.route("/register")
def register():
    return render_template("register.html") 

# Facilities route
@main_bp.route("/facilities")
def facilities():
    return render_template("facilities.html") 

