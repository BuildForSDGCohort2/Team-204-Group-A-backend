"""Set configuration  settings."""

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """Common configuration Setting."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig(Config):
    """Configuration setting at development stage."""

    DEBUG = True


class TestingConfig(Config):
    """Configuration setting at testing stage."""
    TESTING = True


class ProductionConfig(Config):
    """Configuration setting at production stage."""

    DEBUG = False
    TESTING = False


api_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
