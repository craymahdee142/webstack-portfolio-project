from ..extensions import db
from datetime import datetime

class BaseModel(db.Model):
    __abstract__ = True
        
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def save(self):
        """Save current instance"""
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        """Delete the instance"""
        db.session.delete(self)
        db.session.commit()