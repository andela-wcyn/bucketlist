from flask import json
from flask import request, jsonify
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from marshmallow import ValidationError
from marshmallow import post_load
from marshmallow import fields as mfields
from marshmallow import validates

from api.models import User
from . import auth

api = Api(auth)
ma = Marshmallow(auth)


class UserSchema(ma.Schema):
    username = mfields.Str(required=True)
    email = mfields.Email(required=True)
    password = mfields.Str(required=True, load_only=True,
                           error_messages={
                               'required': 'Password is required.'})
    # Smart hyperlinking
    _links = ma.Hyperlinks({
        'self': ma.URLFor('auth.register'),
        'collection': ma.URLFor('bucketlists.bucketlists')
    })

    # @post_load
    # def make_user(self, data):
    #     return User(**data)

    @validates('username')
    def validate_username(self, username):
        if len(username) < 4:
            raise ValidationError('Username must have 4 or more characters.')
        elif len(username) > 20:
            raise ValidationError(
                'Username cannot have more than 20 characters.')
        elif User.username_exists(username):
            raise ValidationError("Username '{}' already exists".format(
                username))

    @validates('email')
    def validate_email(self, email):
        if User.email_exists(email):
            raise ValidationError("The email '{}' is already in use".format(
                email))

    @validates('password')
    def validate_password(self, password):
        if len(password) < 4:
            raise ValidationError('Password must have 4 or more characters.')
        if len(password) > 20:
            raise ValidationError(
                'Password cannot have more than 20 characters.')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

user_fields = {
    'id':   fields.Integer,
    'username':   fields.String,
    'email': fields.String,
    'uri':    fields.Url('auth.register')
}

user_list_fields = {
    'bucketlists':   fields.List(
        fields.Nested(user_fields)
    ),
    'count':   fields.Integer
}


def abort_if_user_doesnt_exist(id=True):
    if not id:
        abort(404, message="Bucketlist '{}' doesn't exist".format(id))


class Register(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('username', dest='username',
                                 location='json',
                                 required=True, type=str,
                                 help='The username is required', )
        self.parser.add_argument('email', dest='email', type=User.valid_email,
                                 location='json',
                                 required=True,
                                 help='The user email is required', )
        self.parser.add_argument('password', dest='password', 
                                 type=User.valid_password,
                                 location='json',
                                 help='Password must have more than 6 characters',
                                 required=True)
        super(Register, self).__init__()

    # @marshal_with(user_fields)
    def post(self):
        print("User!")
        # args = self.parser.parse_args()
        # print("args: ", args, type(args), dict(args), type(dict(args)))

        post_data = json.loads(request.data.decode())
        print("Request decoded: ", post_data, type(post_data))
        data, error = user_schema.load(post_data)
        print("\n\n **result args:  ", data, error)
        if error:
            return error, 400
        user = User(username=post_data['username'], email=post_data['email'],
                    password=post_data['password'])
        user = user.create_user()
        # print("USer: ", user)
        if isinstance(user, User):
            user_data, error = user_schema.dump(data)
            print("User_d: ", user_data, error)
            if error:
                print("Error 2nd: ", error)
                return error, 400
            # return jsonify(user), 201
            return user_data, 201
        return {"message": user}

api.add_resource(Register, '/register')
