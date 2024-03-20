from flask import Blueprint, render_template, redirect, request, url_for, flash
from ..models.maintainance import Maintainance
from ..extensions import db

maintain_bp = Blueprint('maintain_bp', __name__)

@maintain_bp.route("/maintainance")
def maintainance():
    return "This is Maintainance"
