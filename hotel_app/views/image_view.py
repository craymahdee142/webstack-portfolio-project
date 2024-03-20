from flask import Blueprint, render_template, redirect, request, url_for, flash
from ..models.image import Image
from ..extensions import db

image_bp = Blueprint('image_bp', __name__)


@image_bp.route("/image")
def image():
    return "This is Image Model"