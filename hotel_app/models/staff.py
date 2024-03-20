from ..extensions import db
from .base_model import BaseModel
#from sqlalchemy import Sequence

class Staff(BaseModel):
    __tablename__ = 'staff'
    
    # define a sequence for Staff ID number
    #staff_num = Sequence('staff_num', start=1000, increment=1)
    
    #staff_num = db.Column(db.Integer, staff_num, server_default=staff_num.next_value(), nullable=False, unique=True)    
    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(80), nullable=False) # Receptionist, housing keeping, manager
    phone_number = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mailing_address = db.Column(db.String(500), nullable=False)


    def __repr__(self):
        return (f"<Staff(staff_num={self.staff_num}, fullname='{self.fullname}', role='{self.role}', "
                f"phone_number='{self.phone_number}', email='{self.email}')>")