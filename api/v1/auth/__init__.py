from flask import Blueprint

auth = Blueprint('auth', __name__)


# @auth.record
# def record_params(setup_state):
#     app = setup_state.app
#     auth.config = dict([(key, value) for (key, value) in
#                         app.config.iteritems()])

# Import last to prevent Import Error
from . import views

