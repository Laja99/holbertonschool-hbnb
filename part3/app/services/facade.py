from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    # ===== USERS =====
    def create_user(self, user_data):
        existing_user = self.get_user_by_email(user_data["email"])
        if existing_user:
            raise ValueError("Email already registered")

        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute("email", email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        user = self.get_user(user_id)
        if not user:
            return None
        self.user_repo.update(user_id, data)
        return self.get_user(user_id)

    # ===== PLACES =====
    def create_place(self, place_data):

        owner_id = place_data.get("owner_id")
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError("Invalid owner_id: user does not exist")

        amenity_ids = place_data.get("amenities", [])
        amenities = []

        for amenity_id in amenity_ids:
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                raise ValueError(f"Invalid amenity_id: {amenity_id}")
            amenities.append(amenity)

        place = Place(
            title=place_data["title"],
            description=place_data.get("description"),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner_id = owner_id,
            amenities=amenities,
        )

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        if "owner_id" in place_data:
            owner = self.get_user(place_data["owner_id"])
            if not owner:
                raise ValueError("Invalid owner_id: user does not exist")
            place.owner_id = place_data["owner_id"]

        if "amenities" in place_data:
            amenity_ids = place_data.get("amenities", [])
            amenities = []

            for amenity_id in amenity_ids:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError(f"Invalid amenity_id: {amenity_id}")
                amenities.append(amenity)

            place.amenities = amenities

        if "title" in place_data:
            place.title = place_data["title"]

        if "description" in place_data:
            place.description = place_data["description"]

        if "price" in place_data:
            place.price = place_data["price"]

        if "latitude" in place_data:
            place.latitude = place_data["latitude"]

        if "longitude" in place_data:
            place.longitude = place_data["longitude"]

        self.place_repo.update(place_id, place_data)
        return place


    def get_amenities_for_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            return []
        return place.amenities

    def get_reviews_for_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            return []
        return place.reviews

    # ===== AMENITIES =====
    def create_amenity(self, data):
        amenity = Amenity(**data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        self.amenity_repo.update(amenity_id, data)
        return self.get_amenity(amenity_id)

    # ===== REVIEWS =====
    def create_review(self, review_data):
        if "rating" not in review_data:
            raise ValueError("rating is required")

        rating = review_data["rating"]
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")

        if "text" not in review_data or not review_data["text"].strip():
            raise ValueError("Review text cannot be empty")

        user = self.get_user(review_data["user_id"])
        if not user:
            raise ValueError("User not found")

        place = self.get_place(review_data["place_id"])
        if not place:
            raise ValueError("Place not found")

        new_review = Review(
            text=review_data["text"],
            rating=rating,
            user_id=review_data["user_id"],
            place_id=review_data["place_id"],
        )

        self.review_repo.add(new_review)
        place.reviews.append(new_review)
        self.place_repo.update(place.id, {"reviews": place.reviews})

        return new_review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")

        if "text" in review_data:
            text = review_data["text"]
            if not text or not text.strip():
                raise ValueError("Review text cannot be empty")
            review.text = text

        if "rating" in review_data:
            rating = review_data["rating"]
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                raise ValueError("Rating must be an integer between 1 and 5")
            review.rating = rating

        self.review_repo.update(review_id, review_data)
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")

        place = self.get_place(review.place_id)
        if place and review in place.reviews:
            place.reviews.remove(review)
            self.place_repo.update(place.id, {"reviews": place.reviews})
            
        self.review_repo.delete(review_id)

        return True

facade = HBnBFacade()
