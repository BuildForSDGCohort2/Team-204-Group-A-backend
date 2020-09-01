"""Set configuration  settings."""

class Config(object):
    """Common configuration Setting."""
    DEBUG = False
    TESTING = False


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