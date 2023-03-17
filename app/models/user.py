from typing import Union

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_enabled = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, is_enabled=False):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.is_enabled = is_enabled

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_user_by_username(username) -> 'User':
        return User.query.filter_by(username=username).first()

    @staticmethod
    def login(username: str, password: str) -> Union[None, 'User']:
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def register(username: str, password: str) -> 'User':
        user = User(username=username, password=password, is_enabled=True)
        db.session.add(user)
        db.session.commit()
        return user
