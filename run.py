"""
    This file run the api.
"""
import os
from api import create_api

config_name = os.getenv('FLASK_CONFIG')
api = create_api(config_name)

if __name__ == '__main__':
    api.run()
