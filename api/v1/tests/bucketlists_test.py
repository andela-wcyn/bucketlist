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
        self.url = url_for("bucketlists.bucketlists")
        self.expected_data = [BaseTestCase.bucketlist_dict,
                              BaseTestCase.bucketlist2_dict]
        self.get_all()

    # GET /bucketlists/<id> #
    # --------------------- #

    def test_get_bucketlists_id(self):
        """
        Test it returns the correct bucketlist given the id
        """
        self.url = url_for('bucketlists.bucketlistdetails', id=1)
        self.expected_data = BaseTestCase.bucketlist_dict_one
        self.get_one()

    def test_get_bucketlists_id_if_not_exists(self):
        """
        Test it returns 404 not found error if not exists
        """
        self.url = url_for('bucketlists.bucketlistdetails', id=20)
        self.expected_data = {'message': "Bucketlist '20' does not exist. "
                                         "You have requested this URI "
                                         "[/v1/bucketlists/20] but did you "
                                         "mean /v1/bucketlists/<int:id> ?"}
        self.status = 404
        self.get_one(fail=True)

    # GET /bucketlists/<id>/items/ #
    # ---------------------------- #

    def test_get_bucketlists_items(self):
        """
        Test it returns a list of bucketlist items for the bucketlist
        """
        self.url = url_for('bucketlists.bucketlistdetails', id=1)
        self.expected_data = [BaseTestCase.bucketlist_item_dict,
                              BaseTestCase.bucketlist_item2_dict]
        self.get_all()

    def test_get_bucketlists_items_empty_bucketlist(self):
        """
        Test it returns empty list for an empty bucketlist
        """
        self.url = url_for('bucketlists.bucketlistdetails', id=2)
        self.get_all()

    def test_get_bucketlists_items_bucketlist_not_exists(self):
        """
        Test it returns 404 Not Found error when bucketlist does not exist
        """
        self.url = url_for('bucketlists.bucketlists', id=4)
        self.status = 404
        self.get_all()

    # GET /bucketlists/<id>/items/<item_id> #
    # ------------------------------------- #

    def test_get_bucketlists_item(self):
        """
        Test it returns a particular bucketlist item for the bucketlist
        """
        self.url = url_for('bucketlists.bucketlists') + "1/1"
        print("URL: ", self.url)
        self.expected_data = BaseTestCase.bucketlist_item_dict
        self.get_one()

    def test_get_bucketlists_item_not_exists(self):
        """
        Test it returns 404 Not Found Error if item does not exist
        """
        self.url = url_for('bucketlists.bucketlists', id=1, item_id=4)
        self.status = 404
        self.get_one(fail=True)

    def test_get_bucketlists_item_bucketlist_not_exists(self):
        """
        Test it returns 404 Bad Request error when bucketlist does not exist
        """
        self.url = url_for('bucketlists.bucketlists', id=4, item_id=1)
        self.status = 404
        self.get_one()


class BucketlistsPostTestCase(APIPostTestCase):

    # POST /bucketlists/ #
    # ------------------ #

    def test_post_bucketlists(self):
        """
        Test it returns the newly created bucketlist
        """

        self.post_data = {
            "description": "Travel",
            "user": 1
        }
        self.url = url_for('bucketlists.all_bucketlists')
        self.create()

    def test_post_bucketlists_with_wrong_fields(self):
        """
        Test it returns 400 Bad Request error on wrong fields
        """
        self.post_data = {
            "tests": "Travel",
            "test2": 1
        }
        self.url = url_for('bucketlists.all_bucketlists')
        self.status = 400
        self.create(True)

    def test_post_bucketlists_with_missing_fields(self):
        """
        Test it returns 400 Bad Request error on missing fields
        """
        self.post_data = {
            "description": "Travel"
        }
        self.url = url_for('bucketlists.all_bucketlists')
        self.status = 400
        self.create(True)

    # POST /bucketlists/<id>/items/ #
    # ----------------------------- #

    def test_post_bucketlists_items(self):
        """
        Test it returns the newly created bucketlist item
        """
        self.post_data = {
            "description": "Travel to Cairo",
            "bucketlist_id": 1
        }
        self.url = url_for('bucketlists.bucketlists', id=1)
        self.create()

    def test_post_bucketlists_items_with_wrong_fields(self):
        """
        Test it returns 400 Bad Request error on wrong fields
        """
        self.post_data = {
            "tests": "Travel Somewhere",
            "test2": 1
        }
        self.url = url_for('bucketlists.all_bucketlists', id=1)
        self.status = 400
        self.create(True)

    def test_post_bucketlists_item_with_missing_fields(self):
        """
        Test it returns 400 Bad Request error on missing fields
        """
        self.post_data = {
            "description": "Travel to Cairo"
        }
        self.url = url_for('bucketlists.all_bucketlists', id=1)
        self.status = 400
        self.create(True)

    def test_post_bucketlists_item_bucketlist_not_exists(self):
        """
        Test it returns 404 Bad Request error when bucketlist does not exist
        """
        self.post_data = {
            "description": "Travel to Cairo"
        }
        self.url = url_for('bucketlists.all_bucketlists', id=1)
        self.status = 404
        self.create(True)


class BucketlistsPutTestCase(APIPutTestCase):

    # PUT /bucketlists/<id> #
    # --------------------- #

    def test_put_bucketlists_id(self):
        """
        Test it returns the modified bucketlist with the correct changes
        """
        self.put_data = {
            "description": "My Bucketlist modified"
        }
        self.original_data = BaseTestCase.bucketlist_dict
        self.url = url_for('bucketlists.bucketlist', id=1)
        self.modify()

    def test_put_bucketlists_id_not_exists(self):
        """
        Test it returns 404 not found error if not exists
        """
        self.put_data = {
            "description": "My Bucketlist modified"
        }
        self.original_data = BaseTestCase.bucketlist_dict
        self.url = url_for('bucketlists.bucketlist', id=1)
        self.status = 404
        self.modify()

    def test_put_bucketlists_id_wrong_fields(self):
        """
        Test it returns 400 Bad Request error on wrong fields
        """
        self.put_data = {
            "some_field": "My Bucketlist modified"
        }
        self.original_data = BaseTestCase.bucketlist_dict
        self.url = url_for('bucketlists.bucketlist', id=1)
        self.status = 400
        self.modify()


class BucketlistsDeleteTestCase(APIDeleteTestCase):

    # DELETE /bucketlists/<id> #
    # ------------------------ #

    def test_delete_bucketlists_id(self):
        """
        Test it deletes a bucketlist
        """
        url = url_for('bucketlists.bucketlist', id=1)
        self.remove()

    def test_delete_bucketlists_id_not_exists(self):
        """
        Test it returns 404 if Bucketlist does not exist
        """

        url = url_for('bucketlists.bucketlist', id=7)
        status = 404
        self.remove()

