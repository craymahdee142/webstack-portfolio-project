from ..extensions import db
from .base_model import BaseModel


class Image(BaseModel):
    __tablename__ = 'image'
    
    id = db.Column(db.Integer, primary_key=True)

    filename = db.Column(db.String(70), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Image %r>' % self.filename
