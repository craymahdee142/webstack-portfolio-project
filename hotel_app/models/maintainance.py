from ..extensions import db
from .base_model import BaseModel
from datetime import datetime
import uuid


class Maintainance(BaseModel):
    __tablename__ = 'maintainance'
    
    id = db.Column(db.Integer, primary_key=True)

    manitainance_num = db.Column(db.String(50), default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    room_id = db.Column(db.String(50), nullable=False) # Room_id rele
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(1020), nullable=False)
    manitainance_status = db.Column(db.String(80), nullable=False)
    
    
    def __repr__(self):
        # Format the start and end dates for readability
        start_date_formatted = self.start_date.strftime('%Y-%m-%d %H:%M:%S')
        end_date_formatted = self.end_date.strftime('%Y-%m-%d %H:%M:%S')
        return (f"<Maintenance(maintenance_num='{self.maintenance_num}', room_id='{self.room_id}', "
                f"start_date='{start_date_formatted}', end_date='{end_date_formatted}', "
                f"maintenance_status='{self.maintenance_status}')>")
