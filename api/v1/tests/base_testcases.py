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
    token = "token"
    bucketlist_dict = {"description": "My Bucketlist", "user": 1}
    bucketlist2_dict = {"description": "My Bucketlist 2", "user": 1}
    bucketlist_item_dict = {"description": "My Item", "bucketlist": 1}
    bucketlist_item2_dict = {"description": "My Item 2", "bucketlist": 1}

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
                          password='123456781')
        self.user2 = User(username="paul", email="paul@andela.com",
                          password='1234567811')
        self.bucketlist = Bucketlist(description="My Bucketlist",
                                     user=self.user1)
        self.bucketlist2 = Bucketlist(description="My Bucketlist 2",
                                      user=self.user1)

        self.bucketlist_item = BucketlistItem(description="An item")
        self.bucketlist_item2 = BucketlistItem(description="An item 2")

        self.bucketlist.items.append(self.bucketlist_item)
        self.bucketlist.items.append(self.bucketlist_item2)
        self.db.session.add(self.user1)
        self.db.session.add(self.user2)
        self.db.session.add(self.bucketlist)
        self.db.session.add(self.bucketlist2)
        self.db.session.add(self.bucketlist_item)
        self.db.session.add(self.bucketlist_item2)
        self.db.session.commit()

        self.token = self.client.post(url_for('auth.login'),
                         data=json.dumps({"username": "wcyn", "password":
                             "123456781"})).data.decode()
        print("token: ", self.token)

    def tearDown(self):
        """
        Delete all data from the test database
        """
        self.db.session.remove()
        self.db.drop_all()


class APIGetTestCase(BaseTestCase):
    """
    Test abstraction for all the API GET requests
    """
    url = ""
    status = 200
    expected_data = []  # Expected data
    headers = {'Authorization': "JWT " + BaseTestCase.token}

    # def __init__(self):
    # self.headers = {'Authorization': self.token.decode()}

    def get_all(self, status=200):
        """
        :param status: Status expected in the response
        :type status: Integer
        :return:
        :rtype:
        """
        response = self.get_data()
        data_dict = json.loads(response.data)
        self.assertEqual(response.status_code, status)
        self.assertEqual(len(self.expected_data), len(data_dict))

        # Ensure expected data exists in response
        for data in self.expected_data:
            self.assertIn(data, data_dict)
            self.assertIn(data, data_dict)

    def get_one(self):
        """
        :param status: Status expected in the response
        :type status: Integer
        :return:
        :rtype:
        """
        response = self.get_data()
        data_dict = json.loads(response.data)
        self.assertEqual(response.status_code, self.status)

        # Ensure expected data exists in response
        self.assertEqual(self.expected_data, data_dict)

    def get_data(self):
        print('Our header is: ', self.headers)
        if self.headers:
            return self.client.get(self.url,
                                   headers=json.dumps(self.headers))
        else:
            return self.client.get(self.url)


class APIPostTestCase(BaseTestCase):
    """
    Test abstraction for all the API POST requests
    """
    url = ""
    post_data = {}
    status = 201  # Created
    headers = {}

    def create(self, fail=False):
        response = self.post()
        data_dict = json.loads(response.data)
        self.assertEqual(response.status_code, self.status)
        self.assertEqual(self.post_data, data_dict)

        if fail:
            self.assertNotIn(self.post_data, data_dict)

    def post(self):
        if self.headers:
            return self.client.post(self.url,
                                    data=json.dumps(self.post_data),
                                    headers=json.dumps(self.headers))
        else:
            return self.client.post(self.url,
                                    data=json.dumps(self.post_data))


class APIPutTestCase(BaseTestCase):
    """
    Test abstraction for all the API PUT requests
    """
    url = ""
    put_data = {}  # Modified field data
    status = 200
    original_data = {}  # Data before modification
    headers = {}

    def modify(self):
        response = self.put()
        data_dict = json.loads(response.data)
        self.assertEqual(response.status_code, self.status)
        self.assertNotEqual(self.original_data, data_dict)

        # Update original data dict with new fields
        self.original_data.update(self.put_data)
        self.assertEqual(self.original_data, data_dict)

    def put(self):
        if self.headers:
            return self.client.put(self.url,
                                   data=json.dumps(self.put_data),
                                   headers=json.dumps(self.headers))
        else:
            return self.client.put(self.url,
                                   data=json.dumps(self.put_data))


class APIDeleteTestCase(BaseTestCase):
    """
    Test abstraction for all the API DELETE requests
    """
    url = ""
    deleted_data = {}
    status = 204
    headers = {}

    def remove(self):
        response = self.delete()
        self.assertEqual(response.status_code, self.status)
        # Check that object does not exist by GETTING it
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def delete(self):
        if self.headers:
            return self.client.delete(self.url,
                                      headers=json.dumps(self.headers))
        else:
            return self.client.delete(self.url)



