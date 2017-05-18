import os

from flask import Flask
from flask import request
from flask_bcrypt import Bcrypt
from flask_jwt import JWT
from flask_sqlalchemy import SQLAlchemy

from api.config import config_by_name

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWT()


def add_cors_headers(response, ):
    response.headers.add('Access-Control-Allow-Origin', '*')
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    bcrypt.init_app(app)
    from api.models import User
    global jwt
    jwt = JWT(app, User.authenticate, User.identity)

    # Configure version1 blueprint urls
    from api.v1.main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/api/v1')

    from api.v1.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/v1/auth')

    from api.v1.bucketlists import bucketlists as bucketlists_blueprint
    app.register_blueprint(bucketlists_blueprint, url_prefix='/api/v1/bucketlists')

    return app
