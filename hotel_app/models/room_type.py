from ..extensions import db
from .base_model import BaseModel
from sqlalchemy.orm import relationship

class RoomType(BaseModel):
    __tablename__ = 'room_type'
    
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(500), nullable=False, unique=True)
    base_price = db.Column(db.Float, nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)
    amenities = db.Column(db.String(500), nullable=False)
    
    rooms = relationship('Room', back_populates="room_type")

    def __repr__(self):
        return f"<RoomType(id={self.id}, type_name='{self.type_name}', base_price={self.base_price})>"
