from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('places', description='Place operations')

amenity_model = api.model(
    'PlaceAmenity',
    {
        'id': fields.String(description='Amenity ID'),
        'name': fields.String(description='Name of the amenity')
    }
)

user_model = api.model(
    'PlaceUser',
    {
        'id': fields.String(description='User ID'),
        'first_name': fields.String(description='First name'),
        'last_name': fields.String(description='Last name'),
        'email': fields.String(description='Email')
    }
)

review_model = api.model(
    'PlaceReview',
    {
        'id': fields.String(description='Review ID'),
        'text': fields.String(description='Review text'),
        'rating': fields.Integer(description='Rating'),
        'user_id': fields.String(description='User ID')
    }
)

place_model = api.model(
    'Place',
    {
        'title': fields.String(required=True),
        'description': fields.String(),
        'price': fields.Float(required=True),
        'latitude': fields.Float(required=True),
        'longitude': fields.Float(required=True),
        'amenities': fields.List(fields.String, required=False)
    }
)


@api.route('/')
class PlaceList(Resource):

    @api.expect(place_model, validate=True)
    @jwt_required()
    def post(self):
        """Create a new place - authenticated users only"""
        # Get owner_id from JWT token instead of request body
        current_user_id = get_jwt_identity()
        data = request.json
        data['owner_id'] = current_user_id

        try:
            place = facade.create_place(data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": place.owner_id
        }, 201

    def get(self):
        """Retrieve all places - public endpoint"""
        places = facade.get_all_places()

        return [
            {
                "id": p.id,
                "title": p.title,
                "description": p.description,
                "price": p.price,
                "latitude": p.latitude,
                "longitude": p.longitude,
                "owner_id": p.owner_id
            }
            for p in places
        ], 200


@api.route('/<string:place_id>')
class PlaceResource(Resource):

    def get(self, place_id):
        """Retrieve place details - public endpoint"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        owner = facade.get_user(place.owner_id)

        amenities = []
        for a in place.amenities:
            if isinstance(a, str):
                amenity_obj = facade.get_amenity(a)
                if amenity_obj:
                    amenities.append(amenity_obj)
            else:
                amenities.append(a)

        reviews = facade.get_reviews_for_place(place.id)

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": {
                "id": owner.id,
                "first_name": owner.first_name,
                "last_name": owner.last_name,
                "email": owner.email
            } if owner else None,
            "amenities": [
                {"id": am.id, "name": am.name}
                for am in amenities
            ],
            "reviews": [
                {"id": r.id, "text": r.text, "rating": r.rating, "user_id": r.user_id}
                for r in reviews
            ]
        }, 200

    @api.expect(place_model)
    @jwt_required()
    def put(self, place_id):
        """Update a place - owner or admin can modify"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        # Only owner or admin can update
        if not is_admin and place.owner_id != current_user_id:
            return {"error": "Unauthorized action"}, 403

        data = request.json

        try:
            updated = facade.update_place(place_id, data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return {"message": "Place updated successfully"}, 200


@api.route('/<string:place_id>/reviews')
class PlaceReviewList(Resource):

    def get(self, place_id):
        """Get reviews for a place - public endpoint"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        reviews = facade.get_reviews_for_place(place_id)

        return [
            {
                'id': r.id,
                'text': r.text,
                'rating': r.rating,
                'user_id': r.user_id
            }
            for r in reviews
        ], 200