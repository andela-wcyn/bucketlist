from flask import Blueprint
from flask_restful import reqparse

bucketlists = Blueprint('bucketlists', __name__)

# Import last to prevent Import Error
from . import views


# @bucketlists.record
# def record_params(setup_state):
#     app = setup_state.app
#     bucketlists.config = dict([(key, value) for (key, value) in
#                         app.config.iteritems()])
