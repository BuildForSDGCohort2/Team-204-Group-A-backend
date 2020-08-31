"""
    This module initialize the api.
"""
from flask import Flask


# local import
from config import api_config
from api.model import db, bcrypt

# blue print
from api.view.user import user_api as user_blue_print


def create_api(config_name):
    api = Flask(__name__, instance_relative_config=True)
    api.config.from_object(api_config[config_name])
    api.config.from_pyfile('config.py')

    from api.model.user import UserModel


    bcrypt.init_app(api)
    db.init_app(api)

    # registr blue print
    api.register_blueprint(user_blue_print, url_prefix='/api/v1/user')

    # temporary route
    @api.route('/')
    def hello_world():
        return 'Hello, World!'

    return api
    