import os

from config.config import Config


class ProductionConfig(Config):

    ENV = 'prod'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
