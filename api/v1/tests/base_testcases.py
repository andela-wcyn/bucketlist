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

    bucketlist_dict = {"description": "My Bucketlist", "user": 1}
    bucketlist2_dict = {"description": "My Bucketlist 2", "user": 1}
    bucketlist_item_dict = {"description": "My Item", "bucketlist": 1}

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
        self.bucketlist2 = Bucketlist(description="My Bucketlist 2",
                                      user=self.user1)

        self.bucketlist_item = BucketlistItem(description="An item",
                                              bucketlist=self.bucketlist)

        self.db.session.add(self.user1)
        self.db.session.add(self.user2)
        self.db.session.add(self.bucketlist)
        self.db.session.add(self.bucketlist2)
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


class APIGetTestCase(BaseTestCase):
    """
    Test abstraction for all the API GET requests
    """
    url = ""
    expected_data = []  # Expected data
    headers = {}

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

    def get_one(self, status=200):
        """
        :param status: Status expected in the response
        :type status: Integer
        :return:
        :rtype:
        """
        response = self.get_data()
        data_dict = json.loads(response.data)
        self.assertEqual(response.status_code, status)

        # Ensure expected data exists in response
        self.assertEqual(self.expected_data, data_dict)

    def get_data(self):
        if self.headers:
            return self.client.get(self.url,
                                   headers=json.dumps(self.headers))
        else:
            return self.client.get(self.url)


class APIPostTestCase(BaseTestCase):
    """
    Test abstraction for all the API GET requests
    """
    url_pattern = ""
    context = {}  # Expected data
    headers = {}

    def post_data(self):
        return self.client.post(self.url,
                                data=json.dumps(self.context),
                                headers=json.dumps(self.headers))



