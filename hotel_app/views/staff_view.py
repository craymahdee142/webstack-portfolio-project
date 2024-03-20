from flask import Blueprint, render_template, redirect, request, url_for, flash
from ..models.staff import Staff
from ..extensions import db

staff_bp = Blueprint('staff_bp', __name__)

@staff_bp.route("/staff")
def staff():
    return "This is Guest Model"