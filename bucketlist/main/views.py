from flask import jsonify

from . import main


@main.route('/')
def index():
    data = {
        "text": "hello there",
        "color": "blue"
    }
    return jsonify(data)


@main.app_errorhandler(403)
def forbidden(e):
    data = {
        "error": "403",
        "message": "Forbidden"
    }
    return jsonify(data), 403


@main.app_errorhandler(404)
def page_not_found(e):
    data = {
        "error": "404",
        "message": "Page Not Found"
    }
    return jsonify(data), 404


@main.app_errorhandler(500)
def page_not_found(e):
    data = {
        "error": "500",
        "message": "Internal Server Error"
    }
    return jsonify(data), 500
