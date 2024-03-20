from flask import Blueprint, render_template, redirect, request, url_for, flash
from ..models.payment import Payment
from ..extensions import db

payment_bp = Blueprint('payment_bp', __name__)

@payment_bp.route("/payment")
def payment():
    return "This is Payment"
