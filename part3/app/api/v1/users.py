from flask_restx import Namespace, Resource, fields
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
        user_data = api.payload

        try:
            # facade should handle hashing password
            new_user = facade.create_user(user_data)

        except ValueError as e:
            return {"error": str(e)}, 400

        return {
            "id": new_user.id,
            "message": "User created successfully"
        }, 201


    def get(self):
        users = facade.get_all_users()

        return [user.to_dict() for user in users], 200


@api.route('/<string:user_id>')
class UserResource(Resource):

    def get(self, user_id):
        user = facade.get_user(user_id)

        if not user:
            return {"error": "User not found"}, 404

        return user.to_dict(), 200


    @api.expect(update_user_model, validate=True)
    def put(self, user_id):

        try:
            updated_user = facade.update_user(user_id, api.payload)

            if not updated_user:
                return {"error": "User not found"}, 404

            return updated_user.to_dict(), 200

        except ValueError as e:
            return {"error": str(e)}, 400

        except TypeError as e:
            return {"error": str(e)}, 400
