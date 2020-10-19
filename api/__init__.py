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
from api.view.message_view import message_api as message_blue_print
from api.view.apointment_view import appointment_api as appointment_blue_print


def create_api(config_name):
    api = Flask(__name__, instance_relative_config=True)
    api.config.from_object(api_config[config_name])
    api.config.from_pyfile('config.py')

    bcrypt.init_app(api)
    db.init_app(api)
    from .model.blacklist_token import BlacklistToken
    from .model.user import UserModel
    from .model.facility import FacilityModel
    from .model.message import MessageModel
    from .model.appointment import AppointmentModel
    from .model.notification import NotificationModel
    
    jwt = JWTManager(api)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return BlacklistToken.check_blacklist(jti)

    # registr blue print
    api.register_blueprint(user_blue_print, url_prefix='/api/v1/user')
    api.register_blueprint(facility_blue_print, url_prefix='/api/v1/facilities')
    api.register_blueprint(provider_blue_print, url_prefix='/api/v1/provider')
    api.register_blueprint(message_blue_print, url_prefix='/api/v1/messages')
    api.register_blueprint(appointment_blue_print, url_prefix='/api/v1/appointments')

    # temporary route
    @api.route('/')
    def hello_world():
        return 'Hello, World!'

    return api
    