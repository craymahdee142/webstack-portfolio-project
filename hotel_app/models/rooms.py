from ..extensions import db
from .base_model import BaseModel
from sqlalchemy.orm import relationship


class Room(BaseModel):
    __tablename__ = 'room'
    
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String, nullable=False)

    room_status = db.Column(db.String(80), nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)
    amenities = db.Column(db.String(80), nullable=False)
    additional_note = db.Column(db.String(255), nullable=True)
    floor_num = db.Column(db.Integer, nullable=True, unique=True)
    
    room_type_id = db.Column(db.Integer, db.ForeignKey('room_type.id'), nullable=False)
    room_type = relationship('RoomType', back_populates='rooms')
    
    # Reservation relationship
    reservations = relationship('Reservation', back_populates='room', cascade="all, delete", lazy='dynamic')
    
    
    def __repr__(self):
        room_type_name = self.room_type.type_name if self.room_type else 'Unknown'
        return (f"<Room(room_number='{self.room_number}', room_type='{room_type_name}', "
                f"room_status='{self.room_status}', price_per_night={self.price_per_night}, "
                f"amenities='{self.amenities}', additional_note='{self.additional_note}')>")
