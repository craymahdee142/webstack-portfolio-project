from flask import Blueprint, current_app, render_template, redirect, request, url_for, flash
from ..models.reservation import Reservation
from ..models.rooms import Room
from ..models.room_type import RoomType
from ..models.guest import Guest
from ..extensions import db
from datetime import datetime
from sqlalchemy import and_, not_, or_, exists
from flask import session

reserve_bp = Blueprint('reserve_bp', __name__)

# Mapping the room types to their IDs
def get_room_type_mapping():
    if "room_type_mapping" not in session:
        room_types = RoomType.query.all()
        session['room_type_mapping'] = {room_type.type_name.lower(): room_type.id for room_type in room_types}
    return session['room_type_mapping']


@reserve_bp.route("/check_availability", methods=['GET'])
def check_availability():
    check_in_date_str = request.args.get('checkInDate')
    check_out_date_str = request.args.get('checkOutDate')
    print(f"Check-In Date: {check_in_date_str}")
    print(f"Check-Out Date: {check_out_date_str}")

    # Ensure the required date strings are not None
    if not check_in_date_str or not check_out_date_str:
        flash("Missing check-in or check-out date.", "error")
        return redirect(url_for('reserve_bp.index'))  

    # Convert string dates to datetime objects
    try:
        check_in_date = datetime.strptime(check_in_date_str, '%Y-%m-%d')
        check_out_date = datetime.strptime(check_out_date_str, '%Y-%m-%d')
    except ValueError as e:
        flash("Invalid date format. Please use YYYY-MM-DD.", "error")
        return redirect(url_for('reserve_bp.index'))  
    
    
    num_of_adults = request.args.get('numOfAdults')
    num_of_children = request.args.get('numOfChildren', '')
    
    room_type_name = request.args.get('type_name', '').lower()
    room_type_id = get_room_type_mapping().get(room_type_name, None)
    
    
    if room_type_id is None:
        flash("Invalid room type selected", 'error')
        return redirect(url_for("main_bp.home"))
    
    # Fetch room type name for the header
    room_type = RoomType.query.filter_by(id=room_type_id).first()
    if not room_type:
        flash("Room type not found", 'error')
        return redirect(url_for("main_bp.home"))
    
    # Default to page 1, if not provided, acpturing from query params
    page = request.args.get('page', 1, type=int)
    per_page = 8
    
    available_rooms, total_pages, has_prev, has_next = find_available_rooms(room_type_id, 
                                                                            check_in_date, 
                                                                            check_out_date, 
                                                                            page, per_page,
                                                                            num_of_adults,
                                                                            num_of_children,
                                                                            room_type_name
                                                                            )
    
    print(f"Available rooms: {available_rooms}")

    return render_template("available_rooms.html", 
                           rooms=available_rooms, 
                           page=page, 
                           total_pages=total_pages, 
                           has_prev=has_prev, 
                           has_next=has_next,
                           type_name=room_type.type_name)

def find_available_rooms(room_type_id, check_in_date, check_out_date, page, per_page, num_of_adults, num_of_children, room_type_name):
    # EXISTS subquery to check if a room is booked within the requested date range
    booked_rooms_subquery = db.session.query(Reservation.room_number).filter(
        or_(
            and_(
                Reservation.check_in_date <= check_in_date,
                Reservation.check_out_date > check_in_date,
            ),
            and_(
                Reservation.check_in_date < check_out_date,
                Reservation.check_out_date >= check_out_date,
            ),
            and_(
                Reservation.check_in_date >= check_in_date,
                Reservation.check_out_date <= check_out_date,
            ),
        )
    ).correlate(Room).exists()

    # Join Room with RoomType to fetch type name along with room details, considering pagination
    pagination = Room.query.join(RoomType, Room.room_type_id == RoomType.id).add_columns(
        Room.id, Room.room_number, Room.room_status, Room.price_per_night, Room.amenities, Room.additional_note,
        RoomType.type_name
    ).filter(
        Room.room_type_id == room_type_id,
        Room.room_status == 'Available',
        ~booked_rooms_subquery
    ).paginate(page=page, per_page=per_page, error_out=False)

    if not pagination.items and page != 1:
        flash("Requested page is out of range. You have been redirected to the first page.", 'warning')
        return redirect(url_for('reserve_bp.check_availability', checkInDate=check_in_date, checkOutDate=check_out_date, numOfAdults=num_of_adults, numOfChildren=num_of_children, type_name=room_type_name))
  
    # Construct your rooms list here to include the room type name.
    available_rooms = [
        {"room_number": item.room_number, "type_name": item.type_name, "price_per_night": item.price_per_night, "amenities": item.amenities} for item in pagination.items
    ]

    return available_rooms, pagination.pages, pagination.has_prev, pagination.has_next


# Select a room from the available room list
@reserve_bp.route("/select_room/<int:room_id>", methods=['GET'])
def select_room(room_id):
    check_in_date = request.args.get('checkInDate')
    check_out_date = request.args.get('checkOutDate')
    num_of_adults = request.args.get('numOfAdults')
    num_of_children = request.args.get('numOfChildren', '0')
    
    # Store info in session
    session['reservation_details'] = {
        'check_in_date': check_in_date,
        'check_out_date': check_out_date,
        'num_of_adults': num_of_adults,
        'num_of_children': num_of_children,
        'room_id': room_id,
    }
    
    flash("Room selected successfully. Continue to confirm your reservation", 'success')
    return redirect(url_for("reserve_bp.preview_reservation"))


# Preview reservation details
@reserve_bp.route("/preview_reservation", methods=['GET'])
def preview_reservation():
    if 'reservation_details' not in session:
        flash("No reservation details found", 'error')
        return redirect(url_for('reserve_bp.preview_reservation'))
    
    # Retreive reservatrion details from the session
    reservation_details = session['reservation_details']
    guest_id = session.get('guest_id')
    
    room_details = Room.query.get(reservation_details['room_id'])
    
    return render_template('preview_reservation.html', reservation=reservation_details, room=room_details, guest=guest_id)


# Confirm reservation
@reserve_bp.route('/confirm_reservation', methods=['POST'])
def confirm_reservation():
    if 'reservation_details' not in session:
        flash("No reservation details to confirm.", "error")
        return redirect(url_for('reserve_bp.select_room'))

    reservation_details = session.pop('reservation_details', None)

    if not reservation_details:
        flash("Failed to confirm reservation due to missing details.", "error")
        return redirect(url_for('reserve_bp.preview_reservation'))

    # Check if guest_id is available in session 
    guest_id = session.get('guest_id')
    if not guest_id:
        flash("Guest identification is missing.", "error")
        return redirect(url_for('reserve_bp.preview_reservation'))
    
    try:
        guest = Guest.query.get(guest_id)
        print(f"guest_id: {guest_id}")
        
        if not guest:
            raise ValueError("Guest ID not found in session")
            
        # Prepare reservation details   
        check_in_date_str = reservation_details['check_in_date']
        check_out_date_str = reservation_details['check_out_date']
        check_in_date = datetime.strptime(check_in_date_str, '%Y-%m-%d')
        check_out_date = datetime.strptime(check_out_date_str, '%Y-%m-%d')
        
        # Capture Special Request field
        special_req = request.form.get('special_req', '')
    
        new_reservation = Reservation(
            guest_id=guest.id,
            room_id=reservation_details['room_id'],
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            num_of_adults=reservation_details['num_of_adults'],
            num_of_children=reservation_details['num_of_children'],
            special_req=special_req,
            status="pending" # A default status for new reservation
        )

        db.session.add(new_reservation)
        db.session.commit()
            
        flash("Reservation confirmed successfully.", "success")
        return redirect(url_for('reserve_bp.confirm_reservation'))
        
    except Exception as e:
            db.session.rollback()
            flash("An error occurred {e}", "error")
            print(e)
         
           
# Confrim reservation route
@reserve_bp.route("/confirm_reservation")
def confirm():
    return render_template("confirm_reservation.html")

    
