from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

auth_ns = Namespace('auth', description='Authentication operations')

login_model = auth_ns.model('Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

@auth_ns.route('/login')
class LoginResource(Resource):
    @auth_ns.expect(login_model, validate=True)
    def post(self):
        login_data = auth_ns.payload
        user = facade.get_user_by_email(login_data['email'])
        
        if user and user.verify_password(login_data['password']):
            access_token = create_access_token(
                identity=str(user.id), 
                additional_claims={'is_admin': user.is_admin}
            )
            return {'access_token': access_token}, 200
        
        return {'error': 'Invalid email or password'}, 401
