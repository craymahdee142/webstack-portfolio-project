from flask import Blueprint, render_template, redirect, request, url_for, flash
from ..models.rooms import Room
from ..models.room_type import RoomType
from ..extensions import db
from flask_admin import BaseView, expose

# Room BaseView class
class RoomView(BaseView): 
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        room_types = RoomType.query.all()  

        if request.method == 'POST':
            try:
                room_number = request.form['room_number']
                room_status = request.form['room_status']
                price_per_night = request.form['price_per_night']
                amenities = request.form['amenities']
                additional_note = request.form.get('additional_note', '') 
                floor_num = request.form.get('floor_num')  
                room_type_id = request.form.get('room_type_id') 

                # Convert string inputs to their appropriate types
                price_per_night = float(price_per_night) if price_per_night else 0
                floor_num = int(floor_num) if floor_num else None

                new_room = Room(
                    room_number=room_number,
                    room_status=room_status,
                    price_per_night=price_per_night,
                    amenities=amenities,
                    additional_note=additional_note,
                    floor_num=floor_num,
                    room_type_id=room_type_id  # Linking Room to RoomType via room_type_id
                )

                db.session.add(new_room)
                db.session.commit()
                flash("Room added successfully!", 'success')
            except Exception as e:
                db.session.rollback()  
                flash(f"An error occurred: {str(e)}", 'error')

                return redirect(url_for('rooms.index'))  

        # Render the room form template for GET requests
        return self.render('admin/rooms.html', room_types=room_types)