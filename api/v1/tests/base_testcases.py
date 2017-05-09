from flask import json
from flask import url_for
from flask_testing import TestCase

from api import db, create_app
from api.models import User, Bucketlist, BucketlistItem

STATUS_CODES_FAIL = (302, 403, 404)


class BaseTestCase(TestCase):
    """
    Create a Test Database, Set up the required objects and Delete them after
    every test
    """
    bucketlist_dict = {'user': {
        'username': 'wcyn'}, 'description': 'My Bucketlist', '_links': {
        'self': '/v1/bucketlists/1', 'collection': '/v1/bucketlists/'
    }, 'item_count': 2, 'id': 1}
    bucketlist2_dict = {'user': {
        'username': 'wcyn'}, 'description': 'My Bucketlist 2', '_links': {
        'self': '/v1/bucketlists/2', 'collection': '/v1/bucketlists/'
    }, 'item_count': 0, 'id': 2}
    bucketlist_item_dict = {
        'bucketlist_id': 1, 'description': 'An item', 'done': False,
        '_links': {'self': '/v1/bucketlists/1/1',
                   'collection': '/v1/bucketlists/1'}, 'id': 1}
    bucketlist_item2_dict = {
        'bucketlist_id': 1, 'description': 'An item 2', 'done': False,
        '_links': {
            'self': '/v1/bucketlists/1/2',
            'collection': '/v1/bucketlists/1'}, 'id': 2}
    bucketlist_dict_one = {'bucketlist': {
        'description': 'My Bucketlist', 'user': {
            'username': 'wcyn'}, 'item_count': 2, '_links': {
            'self': '/v1/bucketlists/1', 'collection': '/v1/bucketlists/'},
        'id': 1, 'items': [bucketlist_item_dict, bucketlist_item2_dict]}}

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

        self.user1 = User(username="wcyn",
                          email="cynthia.abura@andela.com",
                          password='12345678')
        self.user2 = User(username="paul", email="paul@andela3.com",
                          password='12345678')
        self.bucketlist = Bucketlist(description="My Bucketlist",
                                     user=self.user1)
        self.bucketlist2 = Bucketlist(description="My Bucketlist 2",
                                      user=self.user1)

        self.bucketlist_item = BucketlistItem(description="An item",
                                              bucketlist_id=2)
        self.bucketlist_item2 = BucketlistItem(description="An item 2",
                                               bucketlist_id=2)

        self.db.session.add(self.user1)
        self.db.session.add(self.user2)
        self.db.session.add(self.bucketlist)
        self.db.session.add(self.bucketlist2)
        self.db.session.add(self.bucketlist_item)
        self.db.session.add(self.bucketlist_item2)
        self.bucketlist.items.append(self.bucketlist_item)
        self.bucketlist.items.append(self.bucketlist_item2)
        self.db.session.commit()

        response = self.client.post(
            url_for('auth.login'), data=json.dumps(
                {"username": "wcyn", "password": "12345678"}))
        self.jwt_token = json.loads(response.get_data(as_text=True))["token"]

    def tearDown(self):
        """
        Delete all data from the test database
        """
        self.db.session.remove()
        self.db.drop_all()

    @staticmethod
    def not_exists_message(id="", item_id="", item=False):
        original_item_id = item_id
        if item_id:
            item_id = "/" + item_id
        if item:
            return {'message':
                    "Bucketlist item '{}' does not exist. You have requested "
                    "this URI [/v1/bucketlists/{}{}] but did you mean "
                    "/v1/bucketlists/<int:id> ?".format(
                        original_item_id, id, item_id)}
        else:
            return {'message':
                    "Bucketlist '{}' does not exist. You have requested "
                    "this URI [/v1/bucketlists/{}{}] but did you mean "
                    "/v1/bucketlists/<int:id> ?".format(id, id, item_id)}


class APIGetTestCase(BaseTestCase):
    """
    Test abstraction for all the API GET requests
    """
    url = ""
    status = 200
    expected_data = []  # Expected data
    headers = {"Content-Type": "application/json"}
    token = ""

    # def __init__(self):
    # self.headers = {'Authorization': self.token.decode()}

    def get_all(self, container=None):
        """
        :param status: Status expected in the response
        :type status: Integer
        :return:
        :rtype:
        """
        response = self.get_data()
        data = json.loads(response.data)
        if "data" in data:
            data = data.get("data")
            if isinstance(data, list):
                data = data[0]
            if container:
                for key in container:
                    data = data[key]
        self.assertEqual(response.status_code, self.status)
        self.assertEqual(len(self.expected_data), len(data))

        # Ensure expected data exists in response
        for data_item in self.expected_data:
            self.assertIn(data_item, data)
            self.assertIn(data_item, data)

    def get_one(self):
        """
        :return:
        :rtype:
        """
        response = self.get_data()
        data = json.loads(response.data)
        if "data" in data:
            data = data.get("data")
        self.assertEqual(response.status_code, self.status)

        # Ensure expected data exists in response
        self.assertEqual(self.expected_data, data)

    def get_data(self):
        token = "JWT "
        if self.token:
            token += self.token
        else:
            token += self.jwt_token
        self.headers.update({"Authorization": token})
        if self.headers:
            return self.client.get(self.url,
                                   headers=self.headers)
        else:
            return self.client.get(self.url)


class APIPostTestCase(BaseTestCase):
    """
    Test abstraction for all the API POST requests
    """
    url = ""
    post_data = {}
    expected_data = {}
    status = 201  # Created
    headers = {"Content-Type": "application/json"}
    token = ""

    def create(self):
        response = self.post()
        data_dict = json.loads(response.data)
        self.assertEqual(response.status_code, self.status)
        self.assertEqual(self.expected_data, data_dict)

    def post(self):
        token = "JWT "
        if self.token:
            token += self.token
        else:
            token += self.jwt_token
        self.headers.update({"Authorization": token})
        if self.headers:
            return self.client.post(self.url,
                                    data=json.dumps(self.post_data),
                                    headers=self.headers)
        else:
            return self.client.post(self.url,
                                    data=json.dumps(self.post_data))


class APIPutTestCase(BaseTestCase):
    """
    Test abstraction for all the API PUT requests
    """
    url = ""
    put_data = {}  # Modified field data
    status = 201
    original_data = {}  # Data before modification
    expected_data = {}  # Expected response
    headers = {"Content-Type": "application/json"}
    token = ""

    def modify(self):
        response = self.put()
        data_dict = json.loads(response.data)
        self.assertEqual(response.status_code, self.status)
        self.assertNotEqual(self.original_data, data_dict)
        self.assertEqual(self.expected_data, data_dict)

    def put(self):
        token = "JWT "
        if self.token:
            token += self.token
        else:
            token += self.jwt_token
        self.headers.update({"Authorization": token})
        if self.headers:
            return self.client.put(self.url,
                                   data=json.dumps(self.put_data),
                                   headers=self.headers)
        else:
            return self.client.put(self.url,
                                   data=json.dumps(self.put_data))


class APIDeleteTestCase(BaseTestCase):
    """
    Test abstraction for all the API DELETE requests
    """
    url = ""
    expected_data = {}
    status = 200
    headers = {"Content-Type": "application/json"}
    token = ""

    def remove(self):
        response = self.delete_item()
        # self.assertEqual(response.status_code, self.status)
        # Check that object does not exist by GETTING it
        response = self.client.get(self.url)
        self.assertEqual(response.data, self.expected_data)

    def delete_item(self):
        token = "JWT "
        if self.token:
            token += self.token
        else:
            token += self.jwt_token
        self.headers.update({"Authorization": token})
        if self.headers:
            return self.client.delete(self.url, headers=self.headers)
        else:
            return self.client.delete(self.url)
