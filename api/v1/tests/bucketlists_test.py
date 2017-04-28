from flask import json
from flask import url_for

from .base_testcases import (BaseTestCase, APIGetTestCase,
                             APIPostTestCase, APIPutTestCase,
                             APIDeleteTestCase)


class BucketlistsGetTestCase(APIGetTestCase):

    # GET /bucketlists/ #
    # ----------------- #

    def test_get_bucketlists(self):
        """
        Test it returns a list of bucketlists
        """
        self.url = url_for("bucketlists.all_bucketlists")
        self.expected_data = [BaseTestCase.bucketlist_dict,
                              BaseTestCase.bucketlist2_dict]
        self.get_all()

    # GET /bucketlists/<id> #
    # --------------------- #

    def test_get_bucketlists_id(self):
        """
        Test it returns the correct bucketlist given the id
        """
        self.url = url_for('bucketlists.bucketlist', id=1)
        self.expected_data = BaseTestCase.bucketlist_dict
        self.get_one()

    def test_get_bucketlists_id_if_not_exists(self):
        """
        Test it returns 404 not found error if not exists
        """
        self.url = url_for('bucketlists.bucketlist', id=20)
        self.expected_data = BaseTestCase.bucketlist_dict
        self.status = 404
        self.get_one()

    # GET /bucketlists/<id>/items/ #
    # ---------------------------- #

    def test_get_bucketlists_items(self):
        """
        Test it returns a list of bucketlist items for the bucketlist
        """
        self.url = url_for('bucketlists.bucketlist_items', id=1)
        self.expected_data = [BaseTestCase.bucketlist_item_dict,
                              BaseTestCase.bucketlist_item2_dict]
        self.get_all()

    def test_get_bucketlists_items_empty_bucketlist(self):
        """
        Test it returns empty list for an empty bucketlist
        """
        self.url = url_for('bucketlists.bucketlist_items', id=2)
        self.get_all()

    def test_get_bucketlists_items_bucketlist_not_exists(self):
        """
        Test it returns 404 Not Found error when bucketlist does not exist
        """
        self.url = url_for('bucketlists.bucketlist_items', id=4)
        self.status = 404
        self.get_all()

    # GET /bucketlists/<id>/items/<item_id> #
    # ------------------------------------- #

    def test_get_bucketlists_item(self):
        """
        Test it returns a particular bucketlist item for the bucketlist
        """
        self.url = url_for('bucketlists.bucketlist_items', id=1, item_id=1)
        self.expected_data = BaseTestCase.bucketlist_item_dict
        self.get_one()

    def test_get_bucketlists_item_not_exists(self):
        """
        Test it returns 404 Not Found Error if item does not exist
        """
        self.url = url_for('bucketlists.bucketlist_items', id=1, item_id=4)
        self.status = 404
        self.get_one()

    def test_get_bucketlists_item_bucketlist_not_exists(self):
        """
        Test it returns 404 Bad Request error when bucketlist does not exist
        """
        self.url = url_for('bucketlists.bucketlist_items', id=4, item_id=1)
        self.status = 404
        self.get_one()


class BucketlistsPostTestCase(APIPostTestCase):

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
        self.assertEqual(response.status_code, 201)
        self.assertEqual(new_bucketlist, data_dict)

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

    # POST /bucketlists/<id>/items/ #
    # ----------------------------- #

    def test_post_bucketlists_items(self):
        """
        Test it returns the newly created bucketlist item
        """
        new_bucketlist_item = {
            "description": "Travel to Cairo",
            "bucketlist_id": 1
        }
        response = self.client.post(
            url_for('bucketlists.bucketlist_items', id=1),
            data=json.dumps(new_bucketlist_item)
        )
        data_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(new_bucketlist_item, data_dict)

    def test_post_bucketlists_items_with_wrong_fields(self):
        """
        Test it returns 400 Bad Request error on wrong fields
        """
        new_bucketlist_item = {
            "tests": "Travel Somewhere",
            "test2": 1
        }
        response = self.client.post(
            url_for('bucketlists.bucketlist_items', id=1),
            data=json.dumps(new_bucketlist_item)
        )
        self.assertEqual(response.status_code, 400)
        self.assertNotIn(b'"tests": "Travel"', response.data)
        self.assertNotIn(b'"test2": 1', response.data)

    def test_post_bucketlists_item_with_missing_fields(self):
        """
        Test it returns 400 Bad Request error on missing fields
        """
        new_bucketlist_item = {
            "description": "Travel to Cairo"
        }
        response = self.client.post(
            url_for('bucketlists.bucketlist_items', id=1),
            data=json.dumps(new_bucketlist_item)
        )
        self.assertEqual(response.status_code, 400)
        self.assertNotIn(b'"description": "Travel to Cairo"', response.data)

    def test_post_bucketlists_item_bucketlist_not_exists(self):
        """
        Test it returns 404 Bad Request error when bucketlist does not exist
        """
        new_bucketlist_item = {
            "description": "Travel to Cairo"
        }
        response = self.client.post(
            url_for('bucketlists.bucketlist_items', id=4),
            data=json.dumps(new_bucketlist_item)
        )
        self.assertEqual(response.status_code, 404)


class BucketlistsDeleteTestCase(APIDeleteTestCase):
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
            url_for('bucketlists.bucketlist', id=1))
        self.assertEqual(response.status_code, 204)
        # Check if the bucketlist exists by GETTING it
        response = self.client.get(
            url_for('bucketlists.bucketlist', id=1))
        self.assertEqual(response.status_code, 404)

    def test_delete_bucketlists_id_not_exists(self):
        """
        Test it returns 404 if Bucketlist does not exist
        """

        response = self.client.delete(
            url_for('bucketlists.bucketlist', id=1))
        self.assertEqual(response.status_code, 404)
        # bucketlist = Bucketlist.query.filter_by(id=bucketlist_id)
        # assert not bucketlist


class BucketlistsPutTestCase(APIPutTestCase):
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
            url_for('bucketlists.bucketlist', id=1), data=json.dumps(
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
            url_for('bucketlists.bucketlist', id=1), data=json.dumps(
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
            url_for('bucketlists.bucketlist', id=1), data=json.dumps(
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
            url_for('bucketlists.bucketlist', id=1), data=json.dumps(
                modified_bucketlist))
        data_dict = json.loads(response.data)
        self.assertEqual(error, data_dict)
        self.assertEqual(response.status_code, 400)

