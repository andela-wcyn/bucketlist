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
        self.expected_data = self.not_exists_message("20")
        self.status = 404
        self.get_one()

    # GET /bucketlists/<id>/items/ #
    # ---------------------------- #

    def test_get_bucketlists_items(self):
        """
        Test it returns a list of bucketlist items for the bucketlist
        """
        self.url = url_for('bucketlists.bucketlistdetails', id=1)
        self.expected_data = [BaseTestCase.bucketlist_item_dict,
                              BaseTestCase.bucketlist_item2_dict]
        self.get_all(container=["bucketlist", "items"])

    def test_get_bucketlists_items_empty_bucketlist(self):
        """
        Test it returns empty list for an empty bucketlist
        """
        self.url = url_for('bucketlists.bucketlistdetails', id=2)
        self.get_all(container=["bucketlist", "items"])

    def test_get_bucketlists_items_bucketlist_not_exists(self):
        """
        Test it returns 404 Not Found error when bucketlist does not exist
        """
        self.url = url_for('bucketlists.bucketlists') + "4"
        self.expected_data = self.not_exists_message("4")
        self.status = 404
        self.get_all()

    # GET /bucketlists/<id>/items/<item_id> #
    # ------------------------------------- #

    def test_get_bucketlists_item(self):
        """
        Test it returns a particular bucketlist item for the bucketlist
        """
        self.url = url_for('bucketlists.bucketlists') + "1/1"
        self.expected_data = BaseTestCase.bucketlist_item_dict
        self.get_one()

    def test_get_bucketlists_item_not_exists(self):
        """
        Test it returns 404 Not Found Error if item does not exist
        """
        self.url = url_for('bucketlists.bucketlists') + "1/4"
        self.expected_data = self.not_exists_message("1", "4", item=True)
        self.status = 404
        self.get_one()

    def test_get_bucketlists_item_bucketlist_not_exists(self):
        """
        Test it returns 404 Bad Request error when bucketlist does not exist
        """
        self.url = url_for('bucketlists.bucketlists') + "4/1"
        self.expected_data = {
            'message':
                "Bucketlist '{}' does not exist. You have requested "
                "this URI [/api/v1/bucketlists/{}/{}] but did you mean "
                "/api/v1/bucketlists/<int:id> ?"
                .format(4, 4, 1)}
        self.status = 404
        self.get_one()


class BucketlistsPostTestCase(APIPostTestCase):

    # POST /bucketlists/ #
    # ------------------ #

    def test_post_bucketlists(self):
        """
        Test it returns the newly created bucketlist
        """
        self.post_data = {'description': 'Travel'}
        self.expected_data = {'item_count': 0, 'id': 3, '_links': {
            'self': '/api/v1/bucketlists/3',
            'collection': '/api/v1/bucketlists/'},
                          'description': 'Travel',
                          'user': {'username': self.user1.username}}
        self.url = url_for('bucketlists.bucketlists')
        self.create()

    def test_post_bucketlists_with_wrong_fields(self):
        """
        Test it returns 400 Bad Request error on wrong fields
        """
        self.post_data = {
            "tests": "Travel",
            "test2": 1
        }
        self.expected_data = {'field_errors': {'description': [
            'Description is required.']}}
        self.url = url_for('bucketlists.bucketlists')
        self.status = 400
        self.create()

    def test_post_bucketlists_with_missing_fields(self):
        """
        Test it returns 400 Bad Request error on missing fields
        """
        self.post_data = {}
        self.expected_data = {'field_errors': {'description': [
            'Description is required.']}}
        self.url = url_for('bucketlists.bucketlists')
        self.status = 400
        self.create()

    # POST /bucketlists/<id>/items/ #
    # ----------------------------- #

    def test_post_bucketlists_items(self):
        """
        Test it returns the newly created bucketlist item
        """
        self.post_data = {
            "description": "Travel to Cairo",
            "done": True
        }
        self.expected_data = {'id': 3, 'description': 'Travel to Cairo',
                              'done': True, '_links': {
                                'self': '/api/v1/bucketlists/1/3',
                                'collection': '/api/v1/bucketlists/1'},
                              'bucketlist_id': 1}
        self.url = url_for('bucketlists.bucketlists') + "1"
        self.create()

    def test_post_bucketlists_items_with_wrong_fields(self):
        """
        Test it returns 400 Bad Request error on wrong fields
        """
        self.post_data = {
            "tests": "Travel Somewhere",
            "test2": 1
        }
        self.expected_data = {'field_errors': {'description': [
            'Description is required.']}}
        self.url = url_for('bucketlists.bucketlists') + "1"
        self.status = 400
        self.create()

    def test_post_bucketlists_item_with_missing_fields(self):
        """
        Test it returns 400 Bad Request error on missing fields
        """
        self.post_data = {
            "done": "true"
        }
        self.expected_data = {'field_errors': {'description': [
            'Description is required.']}}
        self.url = url_for('bucketlists.bucketlists') + "1"
        self.status = 400
        self.create()

    def test_post_bucketlists_item_bucketlist_not_exists(self):
        """
        Test it returns 404 Bad Request error when bucketlist does not exist
        """
        self.post_data = {
            "description": "Travel to Cairo"
        }
        self.expected_data = self.not_exists_message("5")
        self.url = url_for('bucketlists.bucketlists') + "5"
        self.status = 404
        self.create()


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
        self.expected_data = {
            'user': {'username': 'wcyn'}, 'id': 1,
            '_links': {'self': '/api/v1/bucketlists/1',
                       'collection': '/api/v1/bucketlists/'},
            'description': 'My Bucketlist modified', 'item_count': 2}
        self.url = url_for('bucketlists.bucketlists') + "1"
        self.modify()

    def test_put_bucketlists_id_not_exists(self):
        """
        Test it returns 404 not found error if not exists
        """
        self.put_data = {
            "description": "My Bucketlist modified"
        }
        self.original_data = BaseTestCase.bucketlist_dict
        self.expected_data = self.not_exists_message("4")
        self.url = url_for('bucketlists.bucketlists') + "4"
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
        self.expected_data = {'field_errors': {'description': [
            'Description is required.']}}
        self.url = url_for('bucketlists.bucketlists') + "1"
        self.status = 400
        self.modify()


class BucketlistsDeleteTestCase(APIDeleteTestCase):

    # DELETE /bucketlists/<id> #
    # ------------------------ #

    def test_delete_bucketlists_id(self):
        """
        Test it deletes a bucketlist
        """

        self.bucketlist_id = 1
        self.url = url_for('bucketlists.bucketlists') + str(self.bucketlist_id)
        print("URL: ", self.url)
        self.expected_data = {"message": "Bucketlist successfully deleted"}
        self.remove()

    def test_delete_bucketlists_id_not_exists(self):
        """
        Test it returns 404 if Bucketlist does not exist
        """

        self.url = url_for('bucketlists.bucketlists') + "7"
        self.expected_data = self.not_exists_message("7")
        self.status = 404
        self.remove()
        pass
