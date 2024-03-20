from flask import Blueprint, render_template, redirect, request, url_for, flash
from ..models.guest import Guest
from ..extensions import db

guest_bp = Blueprint('guset_bp', __name__)

@guest_bp.route("/guest")
def guest():
    return "This is Guest Model"