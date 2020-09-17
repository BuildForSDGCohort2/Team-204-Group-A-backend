"""
    This module initialize the api.
"""
from flask import Flask
from flask_jwt_extended import JWTManager


# local import
from instance.config import api_config
from api.model import db, bcrypt

# blue print
from api.view.user import user_api as user_blue_print
from api.view.facility_view import facility_api as facility_blue_print
from api.view.provider_view import provider_api as provider_blue_print


def create_api(config_name):
    api = Flask(__name__, instance_relative_config=True)
    api.config.from_object(api_config[config_name])
    api.config.from_pyfile('config.py')

    bcrypt.init_app(api)
    db.init_app(api)
    from .model.blacklist_token import BlacklistToken
    from .model.user import UserModel, UserSchema
    from .model.facility import FacilityModel
    
    jwt = JWTManager(api)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return BlacklistToken.check_blacklist(jti)

    # registr blue print
    api.register_blueprint(user_blue_print, url_prefix='/api/v1/user')
    api.register_blueprint(facility_blue_print, url_prefix='/api/v1/facilities')
    api.register_blueprint(provider_blue_print, url_prefix='/api/v1/provider')
    
    # @api.before_first_request
    # def create_admin_user():
    #     db.drop_all()
    #     db.create_all()
    #     # save admin
    #     data = {'firstname' : "User",
    #             'lastname' : "Admin",
    #             'username' : "admin",
    #             'email' : "admin@admin.com",
    #             'password' : "Admin123",
    #             'is_admin' : True}
    #     admin_user = UserModel(data)
        
    #     # admin = UserModel(data)
    #     admin_user.save()

    # temporary route
    @api.route('/')
    def hello_world():
        return 'Hello, World!'

    return api
    