"""
    This module initialize the api.
"""
from flask import Flask

# local import
from instance.config import api_config


def create_api(config_name):
    api = Flask(__name__, instance_relative_config=True)
    api.config.from_object(api_config[config_name])
    api.config.from_pyfile('config.py')

    # temporary route
    @api.route('/')
    def hello_world():
        return 'Hello, World!'

    return api
    