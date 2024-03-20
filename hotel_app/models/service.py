from ..extensions import db
from .base_model import BaseModel
import uuid


class Service(BaseModel):
    __tablename__ = 'service'
    
    id = db.Column(db.Integer, primary_key=True)

    service_num = db.Column(db.String(50), default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    service_name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    price_per_service = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return (f"<Service(service_num='{self.service_num}', service_name='{self.service_name}', "
                f"price_per_service={self.price_per_service})>")
