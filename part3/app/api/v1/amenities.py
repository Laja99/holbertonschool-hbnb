from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services.facade import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model(
    'Amenity',
    {
        'name': fields.String(required=True, description='Name of the amenity')
    }
)


@api.route('/')
class AmenityList(Resource):

    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Create amenity - admin only"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {"error": "Admin privileges required"}, 403

        data = request.json

        try:
            amenity = facade.create_amenity(data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return {"id": amenity.id, "name": amenity.name}, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve all amenities - public endpoint"""
        amenities = facade.get_all_amenities()
        return [{"id": a.id, "name": a.name} for a in amenities], 200


@api.route('/<string:amenity_id>')
class AmenityResource(Resource):

    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Retrieve amenity by ID - public endpoint"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return {"id": amenity.id, "name": amenity.name}, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def put(self, amenity_id):
        """Update amenity - admin only"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {"error": "Admin privileges required"}, 403

        data = request.json

        try:
            updated = facade.update_amenity(amenity_id, data)
        except ValueError as e:
            return {"error": str(e)}, 400

        if not updated:
            return {"error": "Amenity not found"}, 404

        return {"id": updated.id, "name": updated.name}, 200