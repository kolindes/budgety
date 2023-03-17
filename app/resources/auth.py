from flask_jwt_extended import create_access_token
from flask_restful import reqparse, Resource

from app.models import User
from app.response_templates.utils import get_base_response, BaseResponseStatus


class RegistrationResource(Resource):

    def __init__(self):
        self.registration_parser = reqparse.RequestParser()
        self.registration_parser.add_argument('username', type=str, required=True)
        self.registration_parser.add_argument('password', type=str, required=True)
        self.registration_parser.add_argument('is_enabled', type=bool, default=True)
        super(RegistrationResource, self).__init__()

    def post(self):
        response = get_base_response()

        args = self.registration_parser.parse_args()
        errors = []
        username, password = None, None

        try:
            username = args['username']
            usr_len = len(username)
            if usr_len < 3 or usr_len > 15:
                raise ValueError(f'Username length cannot be less then 3 and longer than 15.')
        except ValueError as e:
            errors.append(f'Incorrect username value, got <{args["username"]}>, exc:{e}')

        try:
            password = args['password']
            pwd_len = len(password)
            if pwd_len < 4 or pwd_len > 15:
                raise ValueError(f'Password length cannot be less then 4 and longer than 15.')
        except ValueError as e:
            errors.append(f'Incorrect password value, got <{args["password"]}>, exc:{e}')

        if errors:
            response['status'] = BaseResponseStatus.ERROR
            response['message'] = f'\n'.join(errors)
            return response, 400

        if User.query.filter_by(username=username).first():
            response['status'] = BaseResponseStatus.ERROR
            response['message'] = 'Username already exists'
            return response, 400

        User.register(username, password)

        response['message'] = f'Registration successful for user {username}'

        return response, 200


class LoginResource(Resource):

    def __init__(self):
        self.login_parser = reqparse.RequestParser()
        self.login_parser.add_argument('username', type=str, required=True)
        self.login_parser.add_argument('password', type=str, required=True)

        super(LoginResource, self).__init__()

    def post(self):
        response = get_base_response()

        args = self.login_parser.parse_args()
        errors = []

        username = args['username']
        password = args['password']

        if not username:
            errors.append(f'Incorrect username value, got <{args["username"]}>.')

        if not password:
            errors.append(f'Incorrect password value, got <{args["password"]}>.')

        if errors:
            response['status'] = BaseResponseStatus.ERROR
            response['message'] = f'Errors: '  + f'\n'.join(errors)
            return response, 400

        user = User.login(username, password)

        if user:
            access_token = create_access_token(identity=user.id)
            response['data'] = {'access_token': access_token}
            code = 200

        else:
            response['status'] = BaseResponseStatus.ERROR
            response['message'] = 'Invalid username or password'
            code = 401

        return response, code
