from flask import json
from flask import jsonify, request
from flask_jwt import jwt_required, current_identity
from flask_restful import Api, Resource, reqparse, abort, marshal_with
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError, validates
from marshmallow import fields

from api.error_formatter import ErrorFormatter
from api.models import Bucketlist
from api.v1.auth.views import UserSchema
from . import bucketlists

api = Api(bucketlists)
ma = Marshmallow(bucketlists)
err = ErrorFormatter()

# bucketlist_fields = {
#     'id':   fields.Integer,
#     'description':   fields.String,
#     'uri':    fields.Url('bucketlists.bucketlistdetails')
# }
#
# bucketlist_list_fields = {
#     'bucketlists':   fields.List(
#         fields.Nested(bucketlist_fields)
#     ),
#     'count':   fields.Integer
# }

class BucketlistItemSchema(ma.Schema):
    id = fields.Integer(required=True)
    description = fields.Str(required=True,
                             error_messages={
                               'required': 'Description is required.'})
    user = fields.Nested(UserSchema, exclude=('password',), dump_only=True)
    # Smart hyperlinking
    _links = ma.Hyperlinks({
        'self': ma.URLFor('bucketlists.bucketlists', id='<id>',
                          item_id='<item_id>'),
        'collection': ma.URLFor('bucketlists.bucketlists', id='<id>')
    })

    @validates('description')
    def validate_description(self, description):
        if len(description) > 300:
            raise ValidationError(
                'Description cannot have more than 300 characters.')

    # @post_load
    # def make_user(self, data):
    #     return User(**data)


class BucketlistSchema(ma.Schema):
    id = fields.Integer(required=True)
    description = fields.Str(required=True,
                             error_messages={
                               'required': 'Description is required.'})
    user = fields.Nested(UserSchema, exclude=('password',), dump_only=True)
    items = fields.Nested(BucketlistItemSchema, many=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('bucketlists.bucketlists', id='<id>'),
        'collection': ma.URLFor('bucketlists.bucketlists')
    })
    # @post_load
    # def make_user(self, data):
    #     return User(**data)

    @validates('description')
    def validate_description(self, description):
        if len(description) > 100:
            raise ValidationError(
                'Description cannot have more than 100 characters.')


bucketlist_schema = BucketlistSchema()
bucketlists_schema = BucketlistSchema(many=True)
bucketlist_item_schema = BucketlistItemSchema()
bucketlist_items_schema = BucketlistItemSchema(many=True)


def abort_if_bucketlist_doesnt_exist(id=True):
    if not id:
        abort(404, message="Bucketlist '{}' doesn't exist".format(id))


class Bucketlists(Resource):
    method_decorators = [jwt_required()]

    def get(self):
        print("Current Identity: ", current_identity)
        bucket_lists = Bucketlist.query.filter_by(
            user=current_identity).all()
        print("Bucketlists: ", bucket_lists)
        return bucketlists_schema.dump(bucket_lists)

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
        super(BucketlistDetails, self).__init__()

    # @marshal_with(bucketlist_fields)
    def get(self, id):
        data = {
            "id": id,
            "description": "best day ever yay!",
            "color": "Hue"
        }
        # print("KWARGS: ", kwargs)
        args = self.parser.parse_args()
        print("ARGS:;;: ", args)
        # self.parser.add_argument('key1', type=str)
        # self.parser.add_arguments('key2', type=str)

        return data
        # abort_if_bucketlist_doesnt_exist(1)
        # return data

    def delete(self, **kwargs):
        print("DELETE ID!: ", kwargs)
        abort_if_bucketlist_doesnt_exist(kwargs['id'])
        return '', 204

    # @marshal_with(bucketlist_fields)
    def put(self, **kwargs):
        # print("ARGS: ", id)
        # self.parser.add_argument('key1', type=str)
        # self.parser.add_argument('key2', type=str)
        # abort_if_bucketlist_doesnt_exist(id)
        id = {'id': kwargs['id']}
        print("Putting!", id)
        data = json.loads(request.data)
        print("Data now! ", data)
        return data


class BucketlistItemDetails(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        super(BucketlistItemDetails, self).__init__()

    # @marshal_with(bucketlist_fields)
    def get(self, id):
        data = {
            "id": id,
            "description": "best day ever yay!",
            "color": "Hue"
        }
        # print("KWARGS: ", kwargs)
        args = self.parser.parse_args()
        print("ARGS:;;: ", args)
        # self.parser.add_argument('key1', type=str)
        # self.parser.add_arguments('key2', type=str)

        return data
        # abort_if_bucketlist_doesnt_exist(1)
        # return data

    def delete(self, **kwargs):
        print("DELETE ID!: ", kwargs)
        abort_if_bucketlist_doesnt_exist(kwargs['id'])
        return '', 204

    # @marshal_with(bucketlist_fields)
    def put(self, **kwargs):
        # print("ARGS: ", id)
        # self.parser.add_argument('key1', type=str)
        # self.parser.add_argument('key2', type=str)
        # abort_if_bucketlist_doesnt_exist(id)
        id = {'id': kwargs['id']}
        print("Putting!", id)
        data = json.loads(request.data)
        print("Data now! ", data)
        return data

api.add_resource(Bucketlists, '/')
api.add_resource(BucketlistDetails, '/<int:id>')
api.add_resource(BucketlistItemDetails, '/<int:id>/<int:item_id>')

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
