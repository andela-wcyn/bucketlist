from flask import Blueprint

main = Blueprint('main', __name__)

# Import last to prevent Import Error
from . import views
