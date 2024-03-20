from ..extensions import db
from .base_model import BaseModel
import uuid
from datetime import datetime


class Bookings(BaseModel):
    __tablename__ = 'booking'
    
    id = db.Column(db.Integer, primary_key=True)

    service_num = db.Column(db.String(50), default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    reservation_id = db.Column(db.String(60), nullable=False, unique=True)
    service_id = db.Column(db.String(60), nullable=False, unique=True)
    qty = db.Column(db.Integer, nullable=False)
    booked_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        # Format the booked date for readability
        booked_date_formatted = self.booked_date.strftime('%Y-%m-%d %H:%M:%S')
        return (f"<Bookings(service_num='{self.service_num}', reservation_id='{self.reservation_id}', "
                f"service_id='{self.service_id}', qty={self.qty}, booked_date='{booked_date_formatted}')>")

