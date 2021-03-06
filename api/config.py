import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    HOST = 'localhost'
    # PORT = 5000


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'postgresql://localhost/bucketlist_dev')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'postgresql://localhost/bucketlist_test')


class ProductionConfig(Config):
    DEBUG = False
    HOST = '0.0.0.0'
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'postgresql://localhost/bucketlist')


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
