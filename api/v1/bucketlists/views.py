from flask import json
from flask import jsonify, request
from flask_jwt import jwt_required, current_identity
from flask_restful import Api, Resource, reqparse, abort, marshal_with
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError, validates
from marshmallow import fields
from marshmallow import post_dump
from marshmallow import post_load
from marshmallow import pre_dump
from marshmallow import pre_load

from api.error_formatter import ErrorFormatter
from api.models import Bucketlist, User
from api.v1.auth.views import UserSchema, user_schema
from . import bucketlists

api = Api(bucketlists)
ma = Marshmallow(bucketlists)
err = ErrorFormatter()


class BucketlistItemSchema(ma.Schema):
    """
    Schema used to validate and serialize bucketlist item data
    """
    id = fields.Integer(required=True)
    description = fields.Str(required=True,
                             error_messages={
                               'required': 'Description is required.'})
    user = fields.Nested(UserSchema, exclude=('password', '_links'),
                         dump_only=True)
    bucketlist = fields.Int(required=True, load_only=True)
    # Smart hyperlinking
    _links = ma.Hyperlinks({
        'self': str(ma.URLFor('bucketlists.bucketlists')) + str(id),
        'collection': str(ma.URLFor('bucketlists.bucketlists')) + str(
            bucketlist) + "/" + str(id)
    })

    @validates('description')
    def validate_description(self, description):
        if len(description) > 300:
            raise ValidationError(
                'Description cannot have more than 300 characters.')

    @pre_dump
    def process_bucketlist(self, data):
        print("\n\n &&&&  Postload data: : ", data)
        bucketlist = Bucketlist.query.filter_by(
            bucketlist_id=data['bucketlist']).first()
        if bucketlist:
            print("\n\n%%% Bucketlist stuff ", bucketlist)
            data['bucketlist'] = jsonify(bucketlist).decode()
            return data
        else:
            return err.format_general_errors("Bucketlist Does not Exist")

    # @pre_load(self)
    # @post_load
    # def make_user(self, data):
    #     return User(**data)


class BucketlistSchema(ma.Schema):
    """
    Schema used to validate and serialize bucketlist data
    """
    id = fields.Integer(required=True, dump_only=True)
    description = fields.Str(required=True,
                             error_messages={
                               'required': 'Description is required.'})
    user = fields.Nested(UserSchema, exclude=('password', '_links'),
                         dump_only=True, required=True)
    items = fields.Nested(BucketlistItemSchema, many=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('bucketlists.bucketlists', id='<id>'),
        'collection': ma.URLFor('bucketlists.bucketlists')
    })
    # url = ma.URLFor('bucketlists.bucketlists', id='<id>')
    # print("Link: ", url.__dict__, type(url))
    # @post_load
    # def make_user(self, data):
    #     return User(**data)

    @validates('description')
    def validate_description(self, description):
        if len(description) > 100:
            raise ValidationError(
                'Description cannot have more than 100 characters.')

    @post_dump
    def fix_bucket_link(self, data):
        print("Predump!!", data)
        data['_links']['self'] = data['_links']['collection'] + str(data['id'])
        return data

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
        bucket_lists = Bucketlist.query.filter_by(
            user=current_identity).all()
        print("Bucketlists: ", bucket_lists)
        return bucketlists_schema.dump(bucket_lists)

    def post(self):
        post_data = json.loads(request.data.decode())
        print("Request decoded: ", post_data, type(post_data))
        data, error = bucketlist_schema.load(post_data)
        if error:
            return err.format_field_errors(error)
        bucketlist = Bucketlist(description=post_data['description'],
                                user=current_identity)
        bucketlist = bucketlist.create_bucketlist()
        print("\n\n New Bucketlist!", bucketlist.__dict__)
        if isinstance(bucketlist, Bucketlist):
            print("\n\n New Bucketlist 2!", bucketlist)
            # data.update = 
            user_data, error = user_schema.dump(bucketlist.user)
            if error:
                return err.format_field_errors(error)
            user = {'user': user_data}
            bucketlist_data = bucketlist.__dict__
            bucketlist_data.update(user)
            print("\n\n Data", bucketlist_data)
            # print("\n\n Data id", bucketlist.id)
            bucketlist_data, error = bucketlist_schema.dump(bucketlist)
            if error:
                print("Error 2nd: ", error)
                return err.format_field_errors(error)
            return bucketlist_data, 201
        return err.format_general_errors(
            "An error occurred while creating the bucketlist")


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
