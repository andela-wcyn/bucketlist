from flask import json
from flask import request
from flask_marshmallow import Marshmallow
from flask import current_app as app
from flask_restful import Api, Resource
from marshmallow import ValidationError
from marshmallow import fields
from marshmallow import pre_load
from marshmallow import validates

from api.message_formatter import ErrorFormatter
from api.models import User
from . import auth


api = Api(auth)
ma = Marshmallow(auth)
err = ErrorFormatter()


class UserSchema(ma.Schema):
    """
    Class to serialize User model data for registration
    """
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True,
                          error_messages={
                               'required': 'Password is required.'})

    @validates('username')
    def validate_username(self, username):
        """
        Ensure that username is more that 4 characters and less than 20
        characters
        :param username: Username sent in the response
        :type username: string
        :return: Error if validation requirements not met
        :rtype: ValidationError
        """
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
        """
        Ensure that email does not already exist in the database
        characters
        :param email: email sent in the response
        :type email: string
        :return: Error if validation requirements not met
        :rtype: ValidationError
        """
        if User.email_exists(email):
            raise ValidationError("The email '{}' is already in use".format(
                email))

    @validates('password')
    def validate_password(self, password):
        """
        Ensure that password has more than 6 characters
        :param password: password sent in the response
        :type password: string
        :return: Error if validation requirements not met
        :rtype: ValidationError
        """
        if len(password) < 7:
            raise ValidationError('Password must have more than 6 characters.')


class LoginSchema(ma.Schema):
    """
    Class to serialize User model data for login
    """
    username = fields.Str()
    email = fields.Email()
    password = fields.Str(required=True, load_only=True,
                          error_messages={
                               'required': 'Password is required.'})

    @pre_load
    def ensure_username_or_email_present(self, data):
        if 'email' not in data and 'username' not in data:
            raise ValidationError(
                'You must provide a username or email.')
        return data
user_schema = UserSchema()
login_schema = LoginSchema()


class Register(Resource):
    """
    Create a new user
    """
    @staticmethod
    def post():
        post_data = json.loads(request.data.decode())
        data, error = user_schema.load(post_data)
        if error:
            return err.format_field_errors(error)
        user = User(username=post_data['username'], email=post_data['email'],
                    password=post_data['password'])
        user = user.create_user()
        if isinstance(user, User):
            user_data, error = user_schema.dump(data)
            if error:
                return err.format_field_errors(error)
            return user_data, 201
        return err.format_general_errors(
            "An error occurred while creating the user")


class Login(Resource):
    """
    Login an already registered user
    """
    @staticmethod
    def post():
        post_data = json.loads(request.data.decode())
        user_data, error = login_schema.load(post_data)
        if error:
            return err.format_field_errors(error)
        print("No errors: ", user_data)

        if 'email' in post_data:
            user = User.authenticate(post_data['email'], post_data['password'])
        elif 'username' in post_data:
            user = User.authenticate(post_data['username'],
                                     post_data['password'],
                                     method='username')
        if isinstance(user, User):
            secret = app.config.get('SECRET_KEY')
            token = user.generate_auth_token(secret)
            if token:
                return {"token": token}, 200
            else:
                return err.format_general_errors(
                    "Could not generate token for user")
        else:
            return err.format_general_errors(
                "Login failed. {}".format(user))

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
