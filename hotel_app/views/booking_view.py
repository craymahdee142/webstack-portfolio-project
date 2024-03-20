from flask import Blueprint, render_template, redirect, request, url_for, flash
from ..models.booking import Bookings
from ..extensions import db

book_bp = Blueprint('book_bp', __name__)

@book_bp.route("/booking")
def booking():
    return "This is Booking"
