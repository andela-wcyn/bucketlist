from datetime import datetime

from bucketlist import db


class Bucketlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "<Bookmark '{}': '{}'".format(self.description, self.url)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    bucketlists = db.relationship('Bucketlist', backref='user', lazy='dynamic')

    def __repr__(self):
        return "<User %r" % self.username

