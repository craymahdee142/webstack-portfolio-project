from ..extensions import db
from .base_model import BaseModel
from datetime import datetime
import uuid

class Reservation(BaseModel):
    __tablename__ = 'reservation'

    id = db.Column(db.Integer, primary_key=True)
    reservation_num = db.Column(db.String(50), default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)  # Establishes ForeignKey relationship
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room_number = db.Column(db.Integer, nullable=True, unique=True)
    check_in_date = db.Column(db.DateTime, default=datetime.utcnow)
    check_out_date = db.Column(db.DateTime, default=datetime.utcnow)
    num_of_adults = db.Column(db.Integer, nullable=False)
    num_of_children = db.Column(db.Integer, nullable=False)
    special_req = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(100), nullable=False)

    # Relationship to access guest details from a reservation instance
    guest = db.relationship('Guest', back_populates='reservations')
    room = db.relationship('Room', back_populates='reservations')
    
    def __repr__(self):
        return f"<Reservation(reservation_num={self.reservation_num}, guest_id={self.guest_id}, room_num={self.room_num}, check_in_date={self.check_in_date}, check_out_date={self.check_out_date}, status={self.status})>"

