from flask import jsonify

from . import auth


@auth.route('/login', methods=['POST'])
def login():
    data = {
        "tests": "tests",
    }
    return jsonify(data)


@auth.route('/register', methods=['POST'])
def register():
    data = {
        "tests": "tests",
    }
    return jsonify(data)
