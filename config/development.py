import os

from config.config import Config


class DevelopmentConfig(Config):

    DEBUG = True
    ENV = 'dev'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'dev.db')
