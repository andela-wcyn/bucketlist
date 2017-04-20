from datetime import datetime

from api import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    # password =
    bucketlists = db.relationship('Bucketlist', backref='user', lazy='dynamic')

    def __repr__(self):
        return "<User %r" % self.username


class Bucketlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))
    items = db.relationship('BucketlistItem', backref='api',
                            lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "<Bucketlist '{}': '{}'".format(self.description, self.user_id)


class BucketlistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('api.id'),
                              nullable=False)

    def __repr__(self):
        return "<Bucketlist Item '{}': '{}'".format(
            self.description, self.bucketlist_id)

