from flask import Blueprint

from api import add_cors_headers

bucketlists = Blueprint('bucketlists', __name__)
bucketlists.after_request(add_cors_headers)
# Import last to prevent Import Error
from . import views
