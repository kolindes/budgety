from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

import ssl

from app.response_templates.utils import get_base_response, BaseResponseStatus

db = SQLAlchemy()


def create_app(config_object='config.development.DevelopmentConfig'):
    app = Flask(__name__)
    CORS(app)
    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        response = get_base_response()
        response['status'] = BaseResponseStatus.ERROR
        response['message'] = "Unauthorized access"
        return jsonify(response), 401

    @app.errorhandler(404)
    def page_not_found(e):
        response = get_base_response()
        response['status'] = BaseResponseStatus.NOT_FOUND
        response['message'] = str(e)
        return jsonify(response), 404

    # Load the configuration
    app.config.from_object(obj=config_object)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    from app.routes import (
        auth_resource_bp,
        budgets_bp,
        transactions_bp
    )

    app.register_blueprint(auth_resource_bp)
    app.register_blueprint(budgets_bp)
    app.register_blueprint(transactions_bp)

    with app.app_context():
        db.create_all()

    return app
