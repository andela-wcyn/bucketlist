import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from bucketlist.config import config_by_name

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)

    # Configure version1 blueprint urls
    from bucketlist.v1.main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/v1')

    from bucketlist.v1.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/v1/auth')

    from bucketlist.v1.bucketlists import bucketlists as bucketlists_blueprint
    app.register_blueprint(bucketlists_blueprint, url_prefix='/v1/bucketlists')

    return app


