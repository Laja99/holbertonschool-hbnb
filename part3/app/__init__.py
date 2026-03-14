from flask import Flask
from flask_restx import Api
from .extensions import db, migrate, jwt, bcrypt

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config_class)
    app.config.from_pyfile("config.py", silent=True)
    app.config['PROPAGATE_EXCEPTIONS'] = True

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    @jwt.unauthorized_loader
    def unauthorized_callback(error_string):
        return {"error": "Missing Authorization Header"}, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        return {"error": "Invalid token"}, 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {"error": "Token has expired"}, 401

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API with JWT Authentication',
        doc='/api/v1/'
    )

    try:
        from app.api.v1.users import api as users_ns
        from app.api.v1.amenities import api as amenities_ns
        from app.api.v1.places import api as places_ns
        from app.api.v1.reviews import api as reviews_ns
        from app.api.v1.auth import auth_ns
    except ImportError as e:
        print(f"Error importing namespaces: {e}")
        users_ns = amenities_ns = places_ns = reviews_ns = auth_ns = None

    if auth_ns:
        api.add_namespace(auth_ns, path='/api/v1/auth')
    if users_ns:
        api.add_namespace(users_ns, path='/api/v1/users')
    if amenities_ns:
        api.add_namespace(amenities_ns, path='/api/v1/amenities')
    if places_ns:
        api.add_namespace(places_ns, path='/api/v1/places')
    if reviews_ns:
        api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app