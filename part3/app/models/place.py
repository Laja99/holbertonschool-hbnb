from app.extensions import db
from app.models.base_model import BaseModel


# Many-to-Many association table for Place <-> Amenity
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)


class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # One-to-Many: User owns many Places
    owner = db.relationship('User', backref=db.backref('places', lazy=True))
    # One-to-Many: Place has many Reviews (delete reviews if place is deleted)
    reviews = db.relationship('Review', backref='place', lazy=True, cascade='all, delete-orphan')
    # Many-to-Many: Place has many Amenities
    amenities = db.relationship('Amenity', secondary=place_amenity, backref=db.backref('places', lazy=True))

    def __init__(self, title, price, latitude, longitude, owner_id,
                 description=None, amenities=None, **kwargs):
        super().__init__(**kwargs)

        if not title:
            raise ValueError("Title is required")
        if len(title) > 100:
            raise ValueError("Title cannot exceed 100 characters")
        if price is None or price < 0:
            raise ValueError("Price must be non-negative")
        if latitude is None or not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if longitude is None or not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

        if amenities:
            for amenity in amenities:
                if amenity not in self.amenities:
                    self.amenities.append(amenity)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "amenities": [a.id for a in self.amenities],
            "reviews": [r.id for r in self.reviews],
        })
        return data