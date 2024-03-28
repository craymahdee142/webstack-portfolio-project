from flask import Blueprint, render_template, redirect, request, url_for, flash, current_app
from ..extensions import db
from werkzeug.utils import secure_filename
from flask_login import current_user
from ..models.user import User
from flask_login import login_required, current_user
import os


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = '/path/to/uploads'

image_bp = Blueprint('image_bp', __name__)


# Allowd file
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Upload route
@image_bp.route("/upload", methods=['POST'])
def upload():
    if not current_user.is_authenticated:
        flash("You need to login to access!", 'success')
        return redirect(url_for('main_bp.login'))
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'image' not in request.files:
            flash("No file part")
            return redirect(request.url)
    file = request.files['image']
    # If empty file without filename
    if file.filename == '':
        flash("No selected file")
        return redirect(url_for('main_bp.home'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        file.save(os.path.join(upload_folder, filename))
        
        # Update User profile image in db
        current_user.image = filename
        db.session.commit()
        
        flash("File successfully uploaded", 'success')
        return redirect(url_for('main_bp.home'))
     
     
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=image>
      <input type=submit value=Upload>
    </form>
    '''    

