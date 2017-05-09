from flask import Blueprint
from flask_restful import reqparse

bucketlists = Blueprint('bucketlists', __name__)

# Import last to prevent Import Error
from . import views
