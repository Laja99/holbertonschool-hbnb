from app.extensions import db
from app.models.base_model import BaseModel


class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    # One-to-Many: User has many Reviews
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    # Note: relationship to Place is defined via backref in Place model

    def __init__(self, text, rating, user_id, place_id, **kwargs):
        super().__init__(**kwargs)

        if not text:
            raise ValueError("Review text is required")
        if rating is None or not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        if not user_id:
            raise ValueError("User ID is required")
        if not place_id:
            raise ValueError("Place ID is required")

        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id,
        })
        return data