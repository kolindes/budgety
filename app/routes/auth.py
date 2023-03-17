from flask import Blueprint

from app.resources.auth import RegistrationResource, LoginResource

auth_resource_bp = Blueprint('auth', __name__)

registration_resource = RegistrationResource.as_view('registration_resource')
login_resource = LoginResource.as_view('login_resource')

auth_resource_bp.add_url_rule(
    '/api/auth/registration',
    view_func=registration_resource,
    methods=[
        'POST'
    ]
)

auth_resource_bp.add_url_rule(
    '/api/auth/login',
    view_func=login_resource,
    methods=[
        'POST',
    ]
)
