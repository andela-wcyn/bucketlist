from datetime import datetime

from marshmallow import ValidationError
from sqlalchemy.ext.hybrid import hybrid_property
from validate_email import validate_email

from api import db, bcrypt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    _password = db.Column(db.String(128), nullable=False)
    bucketlists = db.relationship('Bucketlist', backref='user', lazy='dynamic')

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    @staticmethod
    def valid_email(email_str):
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
            return False

    @staticmethod
    def valid_password(pass_str):
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
            raise False

    def validate_user(self):
        if self.username_exists(self.username) or self.email_exists(
                self.email):
            return False
        else:
            return self

    @staticmethod
    def username_exists(username):
        user = User.query.filter_by(username=username).first()
        print("Username Exists or not?: ", user)
        if user:
            print("Yes, exists")
            return True
        print("No, not exists")
        return False

    @staticmethod
    def email_exists(email):
        email = User.query.filter_by(email=email).first()
        if email:
            return True
        return False

    def create_user(self):
        valid_user = self.validate_user()
        if isinstance(valid_user, User):
            db.session.add(self)
            db.session.commit()
        return valid_user

    def __repr__(self):
        return "<User %r>" % self.username


class Bucketlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))
    items = db.relationship('BucketlistItem', backref='bucketlist',
                            lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "<Bucketlist '{}': '{}'>".format(self.description, self.user_id)


class BucketlistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'),
                              nullable=False)

    def __repr__(self):
        return "<Bucketlist Item '{}': '{}'".format(
            self.description, self.bucketlist_id)

