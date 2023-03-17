import os


class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mysecretkey'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwtsecretkey'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
