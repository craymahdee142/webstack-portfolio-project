from ..extensions import db
from .base_model import BaseModel
import uuid

class Review(BaseModel):
    __tablename__ = 'review'
    
    id = db.Column(db.Integer, primary_key=True)

    review_num = db.Column(db.String(50), default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    guest_id = db.Column(db.String(50), nullable=False, unique=True)  # relationship from guest
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(1020), nullable=False)
    
    def __repr__(self):
        # Trim the comment to 50 characters for brevity in the representation
        comment_snippet = (self.comment[:47] + '...') if len(self.comment) > 50 else self.comment
        return (f"<Review(review_num='{self.review_num}', guest_id='{self.guest_id}', "
                f"rating={self.rating}, comment='{comment_snippet}')>")
