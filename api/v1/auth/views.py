from datetime import datetime

from flask import jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from validate_email import validate_email

from api.models import User
from api import db
from . import auth

api = Api(auth)
user_fields = {
    'id':   fields.Integer,
    'username':   fields.String,
    'email': fields.String,
    'uri':    fields.Url('auth.userdetails')
}

user_list_fields = {
    'bucketlists':   fields.List(
        fields.Nested(user_fields)
    ),
    'count':   fields.Integer
}


def email(email_str):
    """
    Return email_str if valid, raise an exception in other case.
    :param email_str:
    :type email_str:
    :return:
    :rtype:
    """
    if validate_email(email_str):
        return email_str
    else:
        raise ValueError('{} is not a valid email'.format(email_str))


def password(pass_str):
    """
    Return pass_str if valid, raise an exception in other case.
    :param pass_str:
    :type pass_str:
    :return:
    :rtype:
    """
    if len(pass_str) > 6:
        return pass_str
    else:
        raise ValueError('{} is not a valid password'.format(pass_str))


def abort_if_user_doesnt_exist(id=True):
    if not id:
        abort(404, message="Bucketlist '{}' doesn't exist".format(id))

# post_parser = reqparse.RequestParser(bundle_errors=True)
# post_parser.add_argument('username', dest='username', location='form',
#                          required=True, type=str,
#                          help='The username is required',)
# post_parser.add_argument('email', dest='email', type=email, location='form',
#                          required=True, help='The user email is required',)
# post_parser.add_argument('password', dest='password', type=password,
#                          location='form',
#                          help='Password must have more than 6 characters',
#                          required=True)


class Register(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('username', dest='username',
                                 location='json',
                                 required=True, type=str,
                                 help='The username is required', )
        self.parser.add_argument('email', dest='email', type=email,
                                 location='json',
                                 required=True,
                                 help='The user email is required', )
        self.parser.add_argument('password', dest='password', type=password,
                                 location='json',
                                 help='Password must have more than 6 characters',
                                 required=True)
        super(Register, self).__init__()

    @marshal_with(user_fields)
    def post(self):
        print("USer!")
        args = self.parser.parse_args()
        print("args:  ", args)
        user = {"hey": "ey"}
        # user = User(username=args['username'], email=args['email'],
        #             password=args['password'])
        # user.create_user()
        return user, 201

api.add_resource(Register, '/register')
