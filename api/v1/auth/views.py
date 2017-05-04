from flask import json
from flask import request
from flask_jwt import JWT, jwt_required
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource, abort
from marshmallow import ValidationError
from marshmallow import fields
from marshmallow import validates

from api.error_handler import ErrorHandler
from api.models import User
from . import auth

api = Api(auth)
ma = Marshmallow(auth)
err = ErrorHandler()


class UserSchema(ma.Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True,
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
        if len(password) < 7:
            raise ValidationError('Password must have more than 6 characters.')


class LoginSchema(ma.Schema):
    username = fields.Str()
    email = fields.Email()
    password = fields.Str(required=True, load_only=True,
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

user_schema = UserSchema()


def abort_if_user_doesnt_exist(id=True):
    if not id:
        abort(404, message="Bucketlist '{}' doesn't exist".format(id))


class Register(Resource):
    # method_decorators = [jwt_required()]

    @staticmethod
    def post():
        post_data = json.loads(request.data.decode())
        # print("Request decoded: ", post_data, type(post_data))
        data, error = user_schema.load(post_data)
        # print("\n\n **result args:  ", data, error)
        if error:
            return err.format_field_errors(error)
        user = User(username=post_data['username'], email=post_data['email'],
                    password=post_data['password'])
        user = user.create_user()
        if isinstance(user, User):
            user_data, error = user_schema.dump(data)
            print("User_d: ", user_data, error)
            if error:
                print("Error 2nd: ", error)
                return err.format_field_errors(error)
            return user_data, 201
        return err.format_general_errors(
            "An error occurred while creating the user")


class Login(Resource):
    @staticmethod
    def post():
        post_data = json.loads(request.data.decode())
        user = None
        if 'email' in post_data:
            user = User.authenticate(post_data['email'], post_data['password'])
        elif 'username' in post_data:
            user = User.authenticate(post_data['username'],
                                     post_data['password'],
                                     method='username')
        # print("Request decoded: ", post_data, type(post_data))
        if isinstance(user, User):
            data, error = user_schema.load(user)
            print("\n\n **result args:  ", data, error)
            if error:
                return err.format_field_errors(error)
            return data, 200
        else:
            return err.format_general_errors(
                "Login failed. {}".format(user))

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
