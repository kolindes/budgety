import os

from config.config import Config


class TestingConfig(Config):

    TESTING = True
    ENV = 'test'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.db')
