from flask import jsonify
from api.v1.main.views import InvalidFieldException

from . import bucketlists


@bucketlists.route('/', methods=['POST', 'GET'])
def all_bucketlists():

    data = [{
        "text": "Bucketlist 1",
        "color": "blue"
    },
        {
        "text": "Bucketlist 2",
        "color": "red"
    }]

    return jsonify(data)


@bucketlists.route('/<id>', methods=['POST', 'GET', 'PUT'])
def bucketlist(id):
    data = {
        "text": "Bucketlist 1",
        "id": int(id)
    }
    return jsonify(data)


@bucketlists.route('/<id>/items', methods=['POST', 'GET'])
def bucketlist_items(id):
    data = [{
        "text": "Bucketlist Item",
        "bucketlist": 1,
        "id": int(id)
    }]
    return jsonify(data)


@bucketlists.route('/<id>/items/<item_id>', methods=['POST', 'GET'])
def bucketlist_item(id, item_id):
    data = [{
        "text": "Bucketlist Item",
        "bucketlist": 1,
        "id": int(id)
    }]
    return jsonify(data)
