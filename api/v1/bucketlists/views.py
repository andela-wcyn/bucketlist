from flask import json
from flask import request
from flask import url_for
from flask_jwt import jwt_required, current_identity
from flask_restful import Api, Resource, abort
from flask_marshmallow import Marshmallow
from marshmallow import (ValidationError, validates, fields, post_dump,
                         post_load)

from api.message_formatter import ErrorFormatter
from api.models import Bucketlist, BucketlistItem
from api.v1.auth.views import UserSchema
from . import bucketlists

api = Api(bucketlists)
ma = Marshmallow(bucketlists)
msg = ErrorFormatter()


def is_valid_json(data):
    try:
        json.loads(data)
    except ValueError:
        return False
    return True


def check_user_permission(user):
    if user != current_identity:
        abort(403, message="Forbidden. You may not view this data")
    return True


def abort_if_bucketlist_doesnt_exist(bucketlist_id):
    bucketlist = Bucketlist.get_bucketlist(bucketlist_id)
    if not bucketlist:
        abort(404, message="Bucketlist '{}' does not exist".format(
            bucketlist_id))
    elif check_user_permission(bucketlist.user):
        return bucketlist


def abort_if_bucketlist_item_doesnt_exist(bucketlist_item_id):
    bucketlist_item = BucketlistItem.get_bucketlist_item(bucketlist_item_id)
    if not bucketlist_item:
        abort(404, message="Bucketlist item '{}' does not exist".format(
            bucketlist_item_id
        ))
    elif check_user_permission(bucketlist_item.bucketlist.user):
        return bucketlist_item


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
        data['user'] = current_identity
        return Bucketlist(**data)

    @validates('description')
    def validate_description(self, description):
        if len(description) > 100:
            raise ValidationError(
                'Description cannot have more than 100 characters.',
                field_names=['description'], fields=['description'])
        elif len(description) < 1:
            raise ValidationError(
                'Description cannot be empty.',
                field_names=['description'], fields=['description'])

    @post_dump
    def fix_bucket_link(self, data):
        # print("Predump!!", data)
        # data['item_count'] = len(data['items'])
        data['_links']['self'] = data['_links']['collection'] + str(data['id'])
        return data


class BucketlistItemSchema(ma.Schema):
    """
    Schema used to validate and serialize bucketlist item data
    """
    id = fields.Integer(required=True, dump_only=True)
    bucketlist_id = fields.Integer(required=True, dump_only=True)
    description = fields.Str(required=True,
                             error_messages={
                               'required': 'Description is required.'})
    done = fields.Boolean(truthy=['t', 'T', 'true', 'True', 'TRUE', '1', 1,
                                  True])
    # Smart hyperlinking
    _links = ma.Hyperlinks({
        'self': ma.URLFor('bucketlists.bucketlists',
                          bucketlist_id='<bucketlist_id>', id='<id>'),
        'collection': ma.URLFor('bucketlists.bucketlists', id='<id>')
    })

    @validates('description')
    def validate_description(self, description):
        if len(description) > 300:
            raise ValidationError(
                'Description cannot have more than 300 characters.',
                field_names=['description'], fields=['description'])
        elif len(description) < 1:
            raise ValidationError(
                'Description cannot be empty.',
                field_names=['description'], fields=['description'])

    @post_dump
    def fix_bucket_item_link(self, data):
        print("\n\n Post dump bucketlist item: ", data)
        if '_links' in data:
            data['_links']['collection'] = '/'.join(
            data['_links']['collection'].split('/')[:-1]) + '/' + str(
            data['bucketlist_id'])
            data['_links']['self'] = data['_links'][
                                     'collection'] + '/' + str(data['id'])
        return data

    @post_load
    def get_bucketlist_item(self, data):
        print("\n\n Post load bucketlist item: ", data)
        return BucketlistItem(**data)

    @staticmethod
    def editable_fields():
        return ['description', 'done']


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
        """
        Get a list of bucketlists from the database
        :return:
        :rtype:
        """
        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=10, type=int)
        bucket_lists = Bucketlist.query.filter_by(
            user=current_identity).paginate(page, limit, error_out=False)
        page_base_url = url_for("bucketlists.bucketlists") + "?"
        return {"data": bucketlists_schema.dump(bucket_lists.items),
                "current_page": bucket_lists.page,
                "has_next": bucket_lists.has_next,
                "has_previous": bucket_lists.has_prev,
                "next_page": page_base_url + "page=" +
                str(bucket_lists.next_num),
                "previous_page": page_base_url + "page=" +
                str(bucket_lists.prev_num),
                "total": bucket_lists.total
                }

    @staticmethod
    def post():
        """
        Add a new bucketlist to the database
        :return:
        :rtype:
        """
        post_data = json.loads(request.data.decode())
        bucketlist, error = bucketlist_schema.load(post_data)
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
        """
        Get the bucketlist with the specified id
        :param id: Bucketlist id from url
        :type id: integer
        :return: Data containing the updated bucketlist or an error message
        :rtype: JSON
        """
        bucketlist = abort_if_bucketlist_doesnt_exist(id)
        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=10, type=int)
        bucketlist_items = BucketlistItem.query.filter_by(
            bucketlist_id=id).paginate(page, limit, error_out=False)
        page_base_url = url_for("bucketlists.bucketlists") + str(id) + "?"
        bucketlist_data, error = bucketlist_schema.dump(bucketlist)
        if error:
            return msg.format_field_errors(error)
        data = {
            'bucketlist': bucketlist_data
        }
        print("Data one: ", data)
        bucketlist_items_data, error = bucketlist_items_schema.dump(
            bucketlist_items.items)
        if error:
            return msg.format_field_errors(error)
        # bucketlist_items_schema.dump(bucketlist_items_data.items)
        data['bucketlist']['items'] = bucketlist_items_data
        print("Data two: ", data['bucketlist'])
        return {"data": data,
                "current_page": bucketlist_items.page,
                "has_next": bucketlist_items.has_next,
                "has_previous": bucketlist_items.has_prev,
                "next_page": page_base_url + "page=" +
                             str(bucketlist_items.next_num),
                "previous_page": page_base_url + "page=" +
                                 str(bucketlist_items.prev_num),
                "total": bucketlist_items.total
                }

    @staticmethod
    def put(id):
        """
        Update the bucketlist with the specified id
        :param id: Bucketlist id from url
        :type id: integer
        :return: Data containing the updated bucketlist or an error message
        :rtype: JSON
        """
        bucketlist = abort_if_bucketlist_doesnt_exist(id)
        put_data = json.loads(request.data.decode())
        put_data['id'] = id
        data, error = bucketlist_schema.dump(put_data)
        if error:
            return msg.format_field_errors(error)
        bucketlist_obj, error = bucketlist_schema.load(put_data)
        if error:
            return msg.format_field_errors(error)
        for key, value in bucketlist_obj.__dict__.items():
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

    @staticmethod
    def post(id):
        """
        Add a new Bucketlist Item to the bucketlist with specified id, to the
        database
        :param id: Bucketlist id from url
        :type id: integer
        :return: Data containing the newly created bucketlist item or an
        error message
        :rtype: JSON
        """
        post_data = json.loads(request.data.decode())
        # print("Request decoded two: ", post_data, type(post_data))
        print("post item data: ", post_data)
        bucketlist_item, error = bucketlist_item_schema.load(post_data)
        if error:
            return msg.format_field_errors(error)

        bucketlist_item = bucketlist_item.create_bucketlist_item(id)
        if isinstance(bucketlist_item, BucketlistItem):
            bucketlist_item_data, error = bucketlist_item_schema.dump(
                bucketlist_item)
            if error:
                return msg.format_field_errors(error)
            return bucketlist_item_data, 201
        return msg.format_general_errors(
            "An error occurred while creating the bucketlist")

    @staticmethod
    def delete(id):
        bucketlist = abort_if_bucketlist_doesnt_exist(id)
        bucketlist.delete_bucketlist()
        return msg.format_success_message(
            "Bucketlist successfully deleted", 200)


class BucketlistItemDetails(Resource):
    method_decorators = [jwt_required()]

    @staticmethod
    def get(id, item_id):
        abort_if_bucketlist_doesnt_exist(id)
        abort_if_bucketlist_item_doesnt_exist(item_id)
        bucket_list_items = BucketlistItem.query.filter_by(
            bucketlist_id=id, id=item_id).first()
        return bucketlist_item_schema.dump(bucket_list_items)

    @staticmethod
    def put(id, item_id):
        abort_if_bucketlist_doesnt_exist(id)
        bucketlist_item = abort_if_bucketlist_item_doesnt_exist(item_id)
        put_data = json.loads(request.data.decode())
        put_data['id'] = item_id
        put_data['bucketlist_id'] = id
        data, error = bucketlist_item_schema.dump(put_data)
        if error:
            return msg.format_field_errors(error)
        # Load so as to validate

        bucketlist_item_object, error = bucketlist_item_schema.load(put_data)
        if error:
            return msg.format_field_errors(error)
        for key, value in bucketlist_item_object.__dict__.items():
            if key in bucketlist_item_schema.editable_fields():
                setattr(bucketlist_item, key, value)
        bucketlist_item = bucketlist_item.update_bucketlist_item()
        if isinstance(bucketlist_item, BucketlistItem):
            bucketlist_item_data, error = bucketlist_item_schema.dump(
                bucketlist_item)
            if error:
                return msg.format_field_errors(error)
            return bucketlist_item_data, 201
        return msg.format_general_errors(
            "An error occurred while updating the bucketlist")

    @staticmethod
    def delete(id, item_id):
        abort_if_bucketlist_doesnt_exist(id)
        bucketlist_item = abort_if_bucketlist_item_doesnt_exist(item_id)
        bucketlist_item.delete_bucketlist_item()
        return msg.format_success_message(
            "Bucketlist item successfully deleted", 200)


api.add_resource(Bucketlists, '/')
api.add_resource(BucketlistDetails, '/<int:id>')
api.add_resource(BucketlistItemDetails, '/<int:id>/<int:item_id>')
