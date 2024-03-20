from flask import Blueprint, render_template, redirect, request, url_for, flash
from ..models.service import Service
from ..extensions import db

service_bp = Blueprint('service_bp', __name__)

@service_bp.route("/service")
def service():
    return "This is Service"
