from flask import jsonify

from . import bucketlists


@bucketlists.route('/', methods=['POST', 'GET'])
def all_bucketlists():
    data = {
        "text": "Bucketlist 1",
        "color": "blue"
    }
    return jsonify(data)


@bucketlists.route('/<id>', methods=['POST', 'GET'])
def bucketlist_item(id):
    data = {
        "text": "Bucketlist 1",
        "id": id
    }
    return jsonify(data)
