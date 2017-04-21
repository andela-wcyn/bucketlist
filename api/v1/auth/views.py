from flask import jsonify

from . import auth


@auth.route('/login', methods=['POST'])
def login():
    data = {
        "test": "test",
    }
    return jsonify(data)


@auth.route('/register', methods=['POST'])
def register():
    data = {
        "test": "test",
    }
    return jsonify(data)
