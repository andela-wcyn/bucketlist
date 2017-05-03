from datetime import datetime

from flask import json
from flask import jsonify, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with

from api.v1.main.views import InvalidFieldException
from . import bucketlists

api = Api(bucketlists)
bucketlist_fields = {
    'id':   fields.Integer,
    'description':   fields.String,
    'uri':    fields.Url('bucketlists.bucketlistdetails')
}

bucketlist_list_fields = {
    'bucketlists':   fields.List(
        fields.Nested(bucketlist_fields)
    ),
    'count':   fields.Integer
}


def abort_if_bucketlist_doesnt_exist(id=True):
    if not id:
        abort(404, message="Bucketlist '{}' doesn't exist".format(id))


class Bucketlists(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('description', type=str,
                                 help='The description cannot be blank ',
                                 location='json',
                                 required=True)
        self.parser.add_argument(
            'date', type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'),
            help='Invalid date type', location='json', required=True)
        super(Bucketlists, self).__init__()

    @marshal_with(bucketlist_list_fields)
    def get(self):
        data = [{
            "text": "id",
            "color": "blue black"
            },
            {
                "text": "Bucketlist 2",
                "color": "red"
            }]
        return jsonify(data)

    def post(self):
        args = self.parser.parse_args()
        # Convert the datetime object back into a string
        args['date'] = args['date'].strftime('%Y-%m-%dT%H:%M:%S')
        print("bucket args: ", args)
        # user = User(username=args['username'], )
        return args, 201


class BucketlistDetails(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=int, required=True,
                                 help='id must be an integer', location='json')
        super(BucketlistDetails, self).__init__()

    @marshal_with(bucketlist_fields)
    def get(self, **kwargs):
        data = {
            "id": kwargs["id"],
            "description": "best day ever yay!",
            "color": "Hue"
        }
        print("KWARGS: ", kwargs)
        # self.parser.add_argument('key1', type=str)
        # self.parser.add_argument('key2', type=str)

        return self.parser.parse_args()
        # abort_if_bucketlist_doesnt_exist(1)
        # return data

    def delete(self, **kwargs):
        print("DELETE ID!: ", kwargs)
        abort_if_bucketlist_doesnt_exist(kwargs['id'])
        return '', 204

    @marshal_with(bucketlist_fields)
    def put(self, **kwargs):
        # print("ARGS: ", id)
        # self.parser.add_argument('key1', type=str)
        # self.parser.add_argument('key2', type=str)
        args = self.parser.parse_args()
        print("ARGS: ", args)
        # abort_if_bucketlist_doesnt_exist(id)
        id = {'id': args['id']}
        print("Putting!", id)
        data = json.loads(request.data)
        print("Data now! ", data)
        return data

api.add_resource(Bucketlists, '/')
api.add_resource(BucketlistDetails, '/<int:id>')

# @bucketlists.route('/', methods=['POST', 'GET'])
# def all_bucketlists():
#
#     data = [{
#         "text": "Bucketlist 1",
#         "color": "blue"
#     },
#         {
#         "text": "Bucketlist 2",
#         "color": "red"
#     }]
#
#     return jsonify(data)
#
#
# @bucketlists.route('/<id>', methods=['POST', 'GET', 'PUT'])
# def bucketlist(id):
#     data = {
#         "text": "Bucketlist 1",
#         "id": int(id)
#     }
#     return jsonify(data)
#
#
# @bucketlists.route('/<id>/items', methods=['POST', 'GET'])
# def bucketlist_items(id):
#     data = [{
#         "text": "Bucketlist Item",
#         "bucketlist": 1,
#         "id": int(id)
#     }]
#     return jsonify(data)
#
#
# @bucketlists.route('/<id>/items/<item_id>', methods=['POST', 'GET'])
# def bucketlist_item(id, item_id):
#     data = [{
#         "text": "Bucketlist Item",
#         "bucketlist": 1,
#         "id": int(id)
#     }]
#     return jsonify(data)
