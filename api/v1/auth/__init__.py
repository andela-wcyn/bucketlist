from flask import Blueprint

auth = Blueprint('auth', __name__)

# Import last to prevent Import Error
from . import views
