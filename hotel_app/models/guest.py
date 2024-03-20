from ..extensions import db
from .base_model import BaseModel
from hotel_app.models.reservation import Reservation


class Guest(BaseModel):
    __tablename__ = 'guest'
    
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(70), nullable=False)
    mailing_address = db.Column(db.String(500), nullable=True)
    identify_proof = db.Column(db.String(70), nullable=True)

    # Relationship to access all reservations made by a guest
    reservations = db.relationship('Reservation', order_by=Reservation.id, back_populates='guest')

    
    def __repr__(self):
        return f"<Guest(fullname='{self.fullname}', email='{self.email}', phone_number='{self.phone_number}')>"