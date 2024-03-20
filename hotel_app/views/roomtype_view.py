from flask import Blueprint, render_template, redirect, request, url_for, flash
from ..models.room_type import RoomType
from ..extensions import db
from flask_admin import BaseView, expose

#froom_type_bp = Blueprint('room_type_bp', __name__)

class RoomTypeView(BaseView):
    @expose("/", methods=('GET', 'POST'))
    def index(self):
        if request.method == 'POST':
            try:
                type_name = request.form.get('type_name')
                description = request.form.get('description')
                base_price = request.form.get('base_price')
                max_capacity = request.form.get('max_capacity')
                amenities = request.form.get('amenities')
                
                # Check for existing room type name
                existing_room_type = RoomType.query.filter_by(type_name=type_name).first()
                if existing_room_type:
                    flash("Room with Type name already exists!", 'error')
                    return redirect(url_for('.index'))
                
                # Create and save the new RoomType instance
                new_room_type = RoomType(
                    type_name=type_name,
                    description=description,
                    base_price=float(base_price),
                    max_capacity=int(max_capacity),
                    amenities=amenities
                )
                    
                db.session.add(new_room_type)
                db.session.commit()
                flash("Room Type added successfully!", 'success')
            except Exception as e:
                db.session.rollback() 
                flash(f'An error occurred: {str(e)}', 'error')               
            
                return redirect(url_for('room_type.index')) 

        return self.render('admin/room_type.html')