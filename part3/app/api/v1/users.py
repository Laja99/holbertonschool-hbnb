from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True, description='Password')
})

update_user_model = api.model('UpdateUser', {
    'first_name': fields.String(),
    'last_name': fields.String(),
    'email': fields.String()
})


@api.route('/')
class UserList(Resource):

    @api.expect(user_model, validate=True)
    def post(self):
        """Register a new user"""
        user_data = api.payload

        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return {
            "id": new_user.id,
            "message": "User created successfully"
        }, 201

    def get(self):
        """Retrieve all users"""
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200


@api.route('/<string:user_id>')
class UserResource(Resource):

    def get(self, user_id):
        """Retrieve a user by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return user.to_dict(), 200

    @api.expect(update_user_model, validate=True)
    @jwt_required()
    def put(self, user_id):
        """Update user profile - only the user themselves can modify their data"""
        # Get authenticated user's ID from JWT token
        current_user_id = get_jwt_identity()

        # Ensure user can only update their own profile
        if current_user_id != user_id:
            return {"error": "Unauthorized action"}, 403

        data = api.payload

        # Block email and password changes for regular users
        if 'email' in data or 'password' in data:
            return {"error": "You cannot modify email or password"}, 400

        try:
            updated_user = facade.update_user(user_id, data)
            if not updated_user:
                return {"error": "User not found"}, 404
            return updated_user.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 400
        except TypeError as e:
            return {"error": str(e)}, 400