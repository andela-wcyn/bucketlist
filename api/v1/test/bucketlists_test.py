from flask import json
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

        self.user1 = User(username="wcyn", email="cynthia.abura@andela.com",
                          password='12345678')
        self.user2 = User(username="paul", email="paul@andela.com",
                          password='12345678')
        self.bucketlist = Bucketlist(description="My Bucketlist",
                                     user=self.user1)
        self.bucketlist_item = BucketlistItem(description="An item",
                                              bucketlist=self.bucketlist)
        self.db.session.add(self.user1)
        self.db.session.add(self.user2)
        self.db.session.add(self.bucketlist)
        self.db.session.add(self.bucketlist_item)
        self.db.session.commit()

        self.client.post(url_for('auth.login'),
                         data=dict(username='wcyn', password='12345678'))

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    # POST /bucketlists/ #
    # ------------------ #

    def test_post_bucketlists_treturns_creaed_bucketlist(self):
        new_bucketlist = {
            "description": "Travel",
            "user": 1
        }
        response = self.client.post(
            url_for('bucketlists.all_bucketlists'),
            data=json.dumps(new_bucketlist)
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'"description": "Travel"', response.data)
        self.assertIn(b'"user": "1"', response.data)

    def test_post_bucketlists_returns_400_error_on_wrong_fields(self):
        new_bucketlist = {
            "test": "Travel",
            "test2": 1
        }
        response = self.client.post(
            url_for('bucketlists.all_bucketlists'),
            data=json.dumps(new_bucketlist)
        )
        self.assertEqual(response.status_code, 400)
        self.assertNotIn(b'"test": "Travel"', response.data)
        self.assertNotIn(b'"test2": 1', response.data)

    def test_post_bucketlists_returns_400_error_on_missing_fields(self):
        new_bucketlist = {
            "description": "Travel"
        }
        response = self.client.post(
            url_for('bucketlists.all_bucketlists'),
            data=json.dumps(new_bucketlist)
        )
        self.assertEqual(response.status_code, 400)
        self.assertNotIn(b'"description": "Travel"', response.data)

    # GET /bucketlists/ #
    # ----------------- #

    def test_get_bucketlists_returns_list_of_bucketlists(self):
        bucketlist2 = Bucketlist(description="My Bucketlist 2",
                                 user=self.user1)
        self.db.session.add(bucketlist2)
        self.db.session.commit()

        response = self.client.get(
            url_for('bucketlists.all_bucketlists')
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'"description": "My Bucketlist"', response.data)
        self.assertIn(b'"description": "My Bucketlist 2"', response.data)
        self.assertEqual(2, len(response.data))

    # GET /bucketlists/<id> #
    # --------------------- #

    def test_get_bucketlists_id_returns_404_error_if_not_exists(self):

        response = self.client.get(
            url_for('bucketlists.bucketlist_item', id=20),

        )
        self.assertEqual(response.status_code, 404)
        self.assertNotIn(b'"description": "My Bucketlist"', response.data)
        self.assertNotIn(b'"description": "My Bucketlist 2"', response.data)

    def test_get_bucketlists_id_returns_correct_bucketlist(self):

        response = self.client.get(
            url_for('bucketlists.bucketlist_item', id=1)
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'"description": "My Bucketlist"', response.data)


# bucketlist = Bucketlist.query.filter_by(id=bucketlist_id)
# assert not bucketlist

# def test_add_furniture(self):
#     new_furniture = {
#                 "furniture_type": "SOFA",
#                 "price": 120000
#             }
#     response = self.client.post("/v1/", data=json.dumps(
#         new_furniture))
#     self.assertEqual(response.status_code, 201)
