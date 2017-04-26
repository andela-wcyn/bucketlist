from flask import json
from flask import url_for
from flask_testing import TestCase

from api import db, create_app
from api.models import User, Bucketlist, BucketlistItem


class BucketlistsTestCase(TestCase):

    def create_app(self):
        """
        Override create app method
        """
        return create_app('test')

    def setUp(self):
        """
        Create objects in the database to use for testing
        """
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
        """
        Delete all data from the test database
        """
        self.db.session.remove()
        self.db.drop_all()

    # POST /bucketlists/ #
    # ------------------ #

    def test_post_bucketlists(self):
        """
        Test it returns the newly created bucketlist
        """
        new_bucketlist = {
            "description": "Travel",
            "user": 1
        }
        response = self.client.post(
            url_for('bucketlists.all_bucketlists'),
            data=json.dumps(new_bucketlist)
        )
        data_dict = json.loads(response.data)
        bucketlist = {"description": "Travel", "user": 1}
        self.assertEqual(response.status_code, 201)
        self.assertEqual(bucketlist, data_dict)

    def test_post_bucketlists_with_wrong_fields(self):
        """
        Test it returns 400 Bad Request error on wrong fields
        """
        new_bucketlist = {
            "tests": "Travel",
            "test2": 1
        }
        response = self.client.post(
            url_for('bucketlists.all_bucketlists'),
            data=json.dumps(new_bucketlist)
        )
        self.assertEqual(response.status_code, 400)
        self.assertNotIn(b'"tests": "Travel"', response.data)
        self.assertNotIn(b'"test2": 1', response.data)

    def test_post_bucketlists_with_missing_fields(self):
        """
        Test it returns 400 Bad Request error on missing fields
        """
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

    def test_get_bucketlists(self):
        """
        Test it returns a list of bucketlists
        """
        bucketlist2 = Bucketlist(description="My Bucketlist 2",
                                 user=self.user1)
        self.db.session.add(bucketlist2)
        self.db.session.commit()

        response = self.client.get(
            url_for('bucketlists.all_bucketlists')
        )
        data_dict = json.loads(response.data)
        bucketlist1 = {"description": "My Bucketlist", "user": 1}
        bucketlist2 = {"description": "My Bucketlist 2", "user": 1}
        self.assertEqual(response.status_code, 200)
        self.assertIn(bucketlist1, data_dict)
        self.assertIn(bucketlist2, data_dict)
        self.assertEqual(2, len(data_dict))

    # GET /bucketlists/<id> #
    # --------------------- #

    def test_get_bucketlists_id(self):
        """
        Test it returns the correct bucketlist given the id
        """
        response = self.client.get(
            url_for('bucketlists.bucketlist_item', id=1)
        )
        data_dict = json.loads(response.data)
        bucketlist = {"description": "My Bucketlist", "user": 1}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(bucketlist, data_dict)

    def test_get_bucketlists_id_if_not_exists(self):
        """
        Test it returns 404 not found error if not exists
        """
        response = self.client.get(
            url_for('bucketlists.bucketlist_item', id=20)
        )
        data_dict = json.loads(response.data)
        bucketlist1 = {"description": "My Bucketlist", "user": 1}
        bucketlist2 = {"description": "My Bucketlist 2", "user": 1}
        self.assertEqual(response.status_code, 404)

    # PUT /bucketlists/<id> #
    # --------------------- #

    def test_put_bucketlists_id(self):
        """
        Test it returns the modified bucketlist with the correct changes
        """
        modified_bucketlist = {
            "description": "My Bucketlist modified"
        }
        response = self.client.put(
            url_for('bucketlists.bucketlist_item', id=1), data=json.dumps(
                modified_bucketlist))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'"description": "My Bucketlist"', response.data)
        self.assertIn(b'"description": "My Bucketlist modified"',
                      response.data)
        self.assertIn(b'"user": "1"', response.data)

    def test_put_bucketlists_id_not_exists(self):
        """
        Test it returns 404 not found error if not exists
        """
        modified_bucketlist = {
            "description": "My Bucketlist modified"
        }
        response = self.client.put(
            url_for('bucketlists.bucketlist_item', id=1), data=json.dumps(
                modified_bucketlist))
        self.assertEqual(response.status_code, 404)

    def test_put_bucketlists_id_wrong_fields(self):
        """
        Test it returns 400 Bad Request error on wrong fields
        """
        modified_bucketlist = {
            "some_field": "My Bucketlist modified"
        }
        response = self.client.put(
            url_for('bucketlists.bucketlist_item', id=1), data=json.dumps(
                modified_bucketlist))
        self.assertEqual(response.status_code, 400)

    def test_put_bucketlists_id_invalid_data(self):
        """
        Test it returns 400 Bad Request error on invalid data
        """
        modified_bucketlist = {
            "some_field": "My Bucketlist modified"
        }
        error = {
            "error": "400",
            "message": "Invalid Data"
        }
        response = self.client.put(
            url_for('bucketlists.bucketlist_item', id=1), data=json.dumps(
                modified_bucketlist))
        data_dict = json.loads(response.data)
        self.assertEqual(error, data_dict)
        self.assertEqual(response.status_code, 400)

        # DELETE /bucketlists/<id> #
        # ------------------------ #

    def test_delete_bucketlists_id(self):
        """
        Test it deletes a bucketlist
        """
        bucketlist = {
            "description": "My Bucketlist"
        }

        response = self.client.delete(
            url_for('bucketlists.bucketlist_item', id=1))
        self.assertEqual(response.status_code, 204)
        # Check if the bucketlist exists by GETTING it
        response = self.client.get(
            url_for('bucketlists.bucketlist_item', id=1))
        self.assertEqual(response.status_code, 404)

    def test_delete_bucketlists_id_not_exists(self):
        """
        Test it returns 404 if Bucketlist does not exist
        """

        response = self.client.delete(
            url_for('bucketlists.bucketlist_item', id=1))
        self.assertEqual(response.status_code, 404)


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
