from datetime import datetime, timedelta
from sqlalchemy.ext.hybrid import hybrid_property
from validate_email import validate_email
import jwt
from api import db, bcrypt


class UserToken(db.Model):
    """
    JWT token model generated when a user logs in
    """
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False,
                        unique=True)

    def __repr__(self):
        return "<User Token '{}': '{}'".format(
            self.user, self.token)


class User(db.Model):
    """
    User data columns to be stored in the database
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    _password = db.Column(db.String(), nullable=False)
    bucketlists = db.relationship('Bucketlist', backref='user',
                                  lazy='dynamic', cascade="all, delete-orphan")

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext).decode()

    @staticmethod
    def valid_email(email_str):
        """
        Return email_str if valid, raise an exception in other case.
        :param email_str: a email to be set for the user
        :type email_str: string
        :return: the validated email or False
        :rtype: str or bool
        """
        if validate_email(email_str):
            return email_str
        else:
            return False

    @staticmethod
    def valid_password(pass_str):
        """
        Return pass_str if valid, raise an exception in other case.
        :param pass_str: a password to be set for the user
        :type pass_str: str
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
        if user:
            return True
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

    def generate_auth_token(self, secret_key, expiration=30000):
        """
        Generate the JWT token used to authenticate the user
        :param secret_key:
        :type secret_key:
        :param expiration:
        :type expiration:
        :return:
        :rtype:
        """
        token = jwt.encode({
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'exp': datetime.utcnow() + timedelta(seconds=expiration),
            'iat': datetime.utcnow(),
            'nbf': datetime.utcnow()
        }, secret_key, algorithm='HS256')
        if token:
            return token.decode()
        return None

    @staticmethod
    def authenticate(identifier, password, method='email'):
        if method == 'email':
            user = User.query.filter_by(email=identifier).first()
        elif method == 'username':
            user = User.query.filter_by(username=identifier).first()
        else:
            return "Internal Error. Invalid identification method"
        if user:
            if bcrypt.check_password_hash(user.password, password):
                return user
            else:
                return "Invalid credentials"
        else:
            return "User '{}' does not exist".format(identifier)

    @staticmethod
    def identity(payload):
        user_id = payload['id']
        return User.query.filter_by(id=user_id).first()

    def __repr__(self):
        return "<User %r>" % self.username


class Bucketlist(db.Model):
    __searchable__ = ['description', 'items']
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300), nullable=False)
    items = db.relationship('BucketlistItem', backref='bucketlist',
                            lazy='dynamic', cascade="all, delete-orphan")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "<Bucketlist '{}': '{}'>".format(self.description, self.user.id)

    def validate_bucketlist(self):
        if len(self.description) > 100:
            return False
        else:
            return self

    def create_bucketlist(self):
        valid_bucketlist = self.validate_bucketlist()
        if isinstance(valid_bucketlist, Bucketlist):
            db.session.add(valid_bucketlist)
            db.session.commit()
            return valid_bucketlist
        else:
            return None

    def update_bucketlist(self):
        valid_bucketlist = self.validate_bucketlist()
        if isinstance(valid_bucketlist, Bucketlist):
            db.session.commit()
        return valid_bucketlist

    def delete_bucketlist(self):
        db.session.delete(self)
        db.session.commit()

    def get_item_count(self):
        return self.items.count()

    @staticmethod
    def get_bucketlist(bucketlist_id):
        bucketlist = Bucketlist.query.filter_by(
            id=bucketlist_id).first()
        return bucketlist


class BucketlistItem(db.Model):
    __searchable__ = ['description']
    id = db.Column(db.Integer, primary_key=True)
    done = db.Column(db.Boolean, default=False, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300), nullable=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'),
                              nullable=False)

    def __repr__(self):
        return "<Bucketlist Item '{}': '{}'>".format(
            self.description, self.bucketlist_id)

    def validate_bucketlist_item(self):
        if len(self.description) > 300 or len(self.description) < 1:
            return False
        else:
            return self

    def create_bucketlist_item(self, bucketlist_id):
        self.bucketlist_id = bucketlist_id
        valid_bucketlist_item = self.validate_bucketlist_item()
        if isinstance(valid_bucketlist_item, BucketlistItem):
            bucketlist = Bucketlist.get_bucketlist(bucketlist_id)
            bucketlist.items.append(self)
            db.session.add(self)
            db.session.commit()
            return self
        else:
            return None

    def update_bucketlist_item(self):
        valid_bucketlist_item = self.validate_bucketlist_item()
        if isinstance(valid_bucketlist_item, BucketlistItem):
            db.session.commit()
        return valid_bucketlist_item

    def delete_bucketlist_item(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_bucketlist_item(bucketlist_item_id):
        bucketlist_item = BucketlistItem.query.filter_by(
            id=bucketlist_item_id).first()
        return bucketlist_item
