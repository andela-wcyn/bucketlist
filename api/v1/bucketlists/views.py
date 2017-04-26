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
def bucketlist_item(id):
    data = {
        "text": "Bucketlist 1",
        "id": int(id)
    }
    return jsonify(data)
