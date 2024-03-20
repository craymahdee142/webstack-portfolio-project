from ..extensions import db
from .base_model import BaseModel
import uuid

class Payment(BaseModel):
    __tablename__ = 'payment'
    
    id = db.Column(db.Integer, primary_key=True)

    payment_num = db.Column(db.String(50), default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    amt = db.Column(db.Float, nullable=False)
    payment_mtd = db.Column(db.String(255), nullable=False)
    payment_status = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return (f"<Payment(reservation_num={self.reservation_num}, amt={self.amt}, "
                f"payment_mtd='{self.payment_mtd}', payment_status='{self.payment_status}')>")
