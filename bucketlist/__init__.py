import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from flask_debugtoolbar import DebugToolbarExtension

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    basedir, 'bucketlist.db')
app.config['DEBUG'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Enable debug toolbar
toolbar = DebugToolbarExtension(app)

# Import last after instantiating db, app and other vars since they are
# required
from bucketlist import models
from bucketlist import views

