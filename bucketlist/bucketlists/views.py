from flask import jsonify

from . import bucketlists


@bucketlists.route('/')
def list_all():
    data = {
        "text": "Bucketlist 1",
        "color": "blue"
    }
    return jsonify(data)


@bucketlists.route('/<id>')
def bucketlist(id):
    data = {
        "text": "Bucketlist 1",
        "id": id
    }
    return jsonify(data)
