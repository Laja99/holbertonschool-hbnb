from app.models.base_model import BaseModel
from app.models.review import Review
from app.models.amenity import Amenity

class Place(BaseModel):
    def __init__(
        self,
        title,
        price,
        latitude,
        longitude,
        owner_id,
        description=None,
        amenities=None,
        reviews=None,
        **kwargs
    ):
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

        if owner_id is None:
            owner_id = ""

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

        self.amenities = amenities or []
        self.reviews = reviews or []

    # Relationship Management Methods
    def add_review(self, review):
        if not isinstance(review, Review):
            raise TypeError("review must be a Review instance")

        if review.place_id != self.id:
            raise ValueError("Review.place_id does not match this Place")

        if review not in self.reviews:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        if not isinstance(amenity, Amenity):
            raise TypeError("amenity must be an Amenity instance")
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
