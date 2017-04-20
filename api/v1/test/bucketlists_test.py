from flask import url_for
from flask_testing import TestCase

from api import db, create_app
from api.models import User, Bucketlist, BucketlistItem


class BucketlistsTestCase(TestCase):

    def create_app(self):
        return create_app('test')

    def setUp(self):
        self.db = db
        self.db.create_all()
        self.client = self.app.test_client()

        user1 = User(username="wcyn", email="cynthia.abura@andela.com",
                     password='12345678')
        user2 = User(username="paul", email="paul@andela.com",
                     password='12345678')
        bucketlist = Bucketlist(description="My Bucketlist", user=user1)
        bucketlist_item = BucketlistItem(description="An item",
                                         bucketlist=bucketlist)
        self.db.session.add(user1)
        self.db.session.add(user2)
        self.db.session.add(bucketlist)
        self.db.session.add(bucketlist_item)
        self.db.session.commit()

        self.client.post(url_for('auth.login'),
                         data=dict(username='wcyn', password='12345678'))

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_delete_bucketlist(self):
        bucketlist_id = 1
        response = self.client.delete(
            url_for('bucketlists.api', bucketlist_id=bucketlist_id),
            follow_redirects=True
        )
        assert response.status_code == 204
        bucketlist = Bucketlist.query.filter_by(id=bucketlist_id)
        assert not bucketlist

