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

from api.message_formatter import ErrorFormatter
from api.models import Bucketlist, User
from api.v1.auth.views import UserSchema, user_schema
from . import bucketlists

api = Api(bucketlists)
ma = Marshmallow(bucketlists)
msg = ErrorFormatter()


def abort_if_bucketlist_doesnt_exist(bucketlist_id):
    bucketlist = Bucketlist.query.filter_by(
        id=bucketlist_id).first()
    if not bucketlist:
        abort(404, message="Bucketlist '{}' doesn't exist".format(
            bucketlist_id))
    else:
        return bucketlist


class BucketlistItemSchema(ma.Schema):
    """
    Schema used to validate and serialize bucketlist item data
    """
    id = fields.Integer(required=True)
    description = fields.Str(required=True,
                             error_messages={
                               'required': 'Description is required.'})
    bucketlist_id = fields.Int(required=True, load_only=True)
    # Smart hyperlinking
    _links = ma.Hyperlinks({
        'self': ma.URLFor('bucketlists.bucketlists', id='<id>'),
        'collection': ma.URLFor('bucketlists.bucketlists', id='<id>',
                                item_id='<item_id>')
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
            return msg.format_general_errors("Bucketlist Does not Exist")

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
    user = fields.Nested(UserSchema, exclude=('password', '_links', 'email'),
                         dump_only=True, required=True)
    item_count = fields.Function(lambda obj: obj.get_item_count())
    _links = ma.Hyperlinks({
        'self': ma.URLFor('bucketlists.bucketlists', id='<id>'),
        'collection': ma.URLFor('bucketlists.bucketlists')
    }, dump_only=True)

    @staticmethod
    def editable_fields():
        return ['description']

    @post_load
    def make_bucketlist(self, data):
        print("Post load bucketlist: ", data)
        data['user'] = current_identity
        return Bucketlist(**data)

    @validates('description')
    def validate_description(self, description):
        if len(description) > 100:
            raise ValidationError(
                'Description cannot have more than 100 characters.')

    @post_dump
    def fix_bucket_link(self, data):
        # print("Predump!!", data)
        # data['item_count'] = len(data['items'])
        data['_links']['self'] = data['_links']['collection'] + str(data['id'])
        return data


class BucketlistDetailsSchema(BucketlistSchema):
    items = fields.Nested(BucketlistItemSchema, many=True)

bucketlist_schema = BucketlistSchema()
bucketlists_schema = BucketlistSchema(many=True)
bucketlist_details_schema = BucketlistDetailsSchema()
bucketlist_item_schema = BucketlistItemSchema()
bucketlist_items_schema = BucketlistItemSchema(many=True)


class Bucketlists(Resource):
    method_decorators = [jwt_required()]

    @staticmethod
    def get():
        bucket_lists = Bucketlist.query.filter_by(
            user=current_identity).all()
        return bucketlists_schema.dump(bucket_lists)

    @staticmethod
    def post():
        post_data = json.loads(request.data.decode())
        # print("Request decoded two: ", post_data, type(post_data))
        bucketlist, error = bucketlist_schema.load(post_data)
        print("bucketlist: ", bucketlist.__dict__)
        if error:
            return msg.format_field_errors(error)
        bucketlist = bucketlist.create_bucketlist()
        if isinstance(bucketlist, Bucketlist):
            bucketlist_data, error = bucketlist_schema.dump(bucketlist)
            if error:
                return msg.format_field_errors(error)
            return bucketlist_data, 201
        return msg.format_general_errors(
            "An error occurred while creating the bucketlist")


class BucketlistDetails(Resource):
    method_decorators = [jwt_required()]

    @staticmethod
    def get(id):
        bucketlist = abort_if_bucketlist_doesnt_exist(id)
        return bucketlist_details_schema.dump(bucketlist)

    @staticmethod
    def delete(id):
        bucketlist = abort_if_bucketlist_doesnt_exist(id)
        bucketlist.delete_bucketlist()
        return msg.format_success_message(
            "Bucketlist successfully deleted", 200)

    @staticmethod
    def put(id):
        bucketlist = abort_if_bucketlist_doesnt_exist(id)
        put_data = json.loads(request.data.decode())
        put_data['id'] = id
        data, error = bucketlist_schema.dump(put_data)
        print("Data from put: ", data)
        if error:
            return msg.format_field_errors(error)
        for key, value in data.items():
            if key in bucketlist_schema.editable_fields():
                setattr(bucketlist, key, value)
        bucketlist = bucketlist.update_bucketlist()
        if isinstance(bucketlist, Bucketlist):
            bucketlist_data, error = bucketlist_schema.dump(bucketlist)
            if error:
                return msg.format_field_errors(error)
            return bucketlist_data, 201
        return msg.format_general_errors(
            "An error occurred while updating the bucketlist")


class BucketlistItemDetails(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        super(BucketlistItemDetails, self).__init__()

    def get(self, id):
        abort_if_bucketlist_doesnt_exist(1)
        return None

    def delete(self, **kwargs):
        print("DELETE ID!: ", kwargs)
        abort_if_bucketlist_doesnt_exist(kwargs['id'])
        return '', 204

    def put(self, **kwargs):
        abort_if_bucketlist_doesnt_exist(id)
        id = {'id': kwargs['id']}
        print("Putting!", id)
        data = json.loads(request.data)
        print("Data now! ", data)
        return data

api.add_resource(Bucketlists, '/')
api.add_resource(BucketlistDetails, '/<int:id>')
api.add_resource(BucketlistItemDetails, '/<int:id>/<int:item_id>')
