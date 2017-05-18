from flask import Blueprint

from api import add_cors_headers

auth = Blueprint('auth', __name__)
auth.after_request(add_cors_headers)
# Import last to prevent Import Error
from . import views
