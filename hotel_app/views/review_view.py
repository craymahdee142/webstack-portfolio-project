from flask import Blueprint, render_template, redirect, request, url_for, flash
from ..models.review import Review
from ..extensions import db

review_bp = Blueprint('review_bp', __name__)

@review_bp.route("/review")
def review():
    return "This is Review"
