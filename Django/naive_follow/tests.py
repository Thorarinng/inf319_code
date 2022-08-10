from django.test import TestCase

# Create your tests here.

from django.test import SimpleTestCase, Client
import json
# TESTING STUFF
# https://docs.djangoproject.com/en/3.1/topics/testing/tools/
from follow.models import Follow


class FollowTestCase(SimpleTestCase):
    databases = "__all__"

    def setUp(self):
        # Used to run tests
        self.client = Client()
        # Login uri
        self.login_uri = '/api/user/login/'
        # The user that will be followed
        self.followUser = '/api/follow/'
        self.register_uri = '/api/user/register/'
        self.buyEquityUrl = '/api/transactions/'
        self.user = {}
        self.followUrl = '/api/follow/'
        self.response = {}
        self.discoverPeopleToFollow = '/api/follow/discover/all/'
        # Followees of symbol
        self.followEquity = '/api/follow/equity/'

        # Authorization headers and tokens
        self.bearer_token = ''
        self.headers1 = ''
        self.tokens = ''
        self._setupUsers()
        # This is a test user that owns certain standardEquity
        self.testUser3 = '/api/follow/test2/'

        self.uriGetFollowersOfEquitySuccessCase = '/api/follow/equity/fb/'
        self.uriGetFollowersOfEquityFailCase = '/api/follow/equity/gme/'
    # FOllow user test
    # Example of call: http://localhost:8000/api/follow/totisg/

    def _setupUsers(self):
        body1 = {
            "email": "test1@gmail.com",
            "password": "test1234",
        }

        self.res1 = self.login(body1)
        self.user1 = self.res1.data
        self.headers1 = self.genToken(self.res1)

        body2 = {
            "email": "test2@gmail.com",
            "password": "test1234",
        }

        self.res2 = self.login(body2)
        self.user2 = self.res2.data
        self.headers2 = self.genToken(self.res2)

    def login(self, body):
        response = self.client.post(self.login_uri, body)
        return response

    def genToken(self, response):
        ''' Access the token from a response '''
        user = response.data
        self.tokens = user['tokens']
        self.bearer_token = self.tokens['access']
        return {"Authorization": f"Bearer {self.bearer_token}"}
    def serialize_json(self, res):
        try:
            try:
                d = json.loads(res.content.decode("utf-8"))['posts']
            except:
                d = json.loads(res.content.decode("utf-8"))
            return d
        except:
            print("crash")

    def test_follow_user_body(self):
        ''' Test follow user body'''
        followUrl = self.followUrl + 'test2' + '/'
        res = self.client.post(
            followUrl, HTTP_AUTHORIZATION=self.headers1["Authorization"])
        d = self.serialize_json(res)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(type(d['isFollowing']), bool)
        res = self.client.post(
            followUrl, HTTP_AUTHORIZATION=self.headers1["Authorization"])
        d = self.serialize_json(res)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(type(d['isFollowing']), bool)

    def test_follow_user(self):
        ''' Test following a user '''
        followUrl = self.followUrl + 'test2' + '/'
        res = self.client.post(
            followUrl, HTTP_AUTHORIZATION=self.headers1["Authorization"])
        d = self.serialize_json(res)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(d['isFollowing'], True)
        res = self.client.post(
            followUrl, HTTP_AUTHORIZATION=self.headers1["Authorization"])
        d = self.serialize_json(res)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(d['isFollowing'], False)
        res = self.client.post(
            followUrl, HTTP_AUTHORIZATION=self.headers1["Authorization"])
        d = self.serialize_json(res)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(d['isFollowing'], True)
        res = self.client.post(
            followUrl, HTTP_AUTHORIZATION=self.headers1["Authorization"])
        d = self.serialize_json(res)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(d['isFollowing'], False)


    def _followEquity(self):
        ''' Follows an equity using the second user '''
        body = {
            "name": "Facebook Inc",
            "symbol": "FB",
            "costBasis": 112.5,
            "amountOfShares": 4,
            "buy": True
        }
        return self.client.post(self.followEquity, body, HTTP_AUTHORIZATION=self.headers2['Authorization'])

    def test_get_followees_of_symbol(self):
        ''' Test to see if we can get every single user that follows a certain equity'''
        followUrl = self.followUrl + 'test2' + '/'
        res = self.client.post(
            followUrl, HTTP_AUTHORIZATION=self.headers1["Authorization"])
        res = self._followEquity()
        d = self.serialize_json(res)
        res = self.client.get(self.followEquity + 'FB/', HTTP_AUTHORIZATION=self.headers2['Authorization'])
        d = self.serialize_json(res)
        self.assertEqual(d['users'], [])
        res = self.client.get(self.followEquity + 'FB/', HTTP_AUTHORIZATION=self.headers1['Authorization'])
        d = self.serialize_json(res)
        followUrl = self.followUrl + 'test2' + '/'
        self.client.post(
            followUrl, HTTP_AUTHORIZATION=self.headers1["Authorization"])
    def test_discover_people_to_follow(self):
        ''' Tests the endpoint that returns some amount of users back for the user to follow, there we can only test that the body is correct'''
        res = self.client.get(
            self.discoverPeopleToFollow, HTTP_AUTHORIZATION=self.headers1["Authorization"])
        for user in res.data['User']:
            self.assertEqual(True, 'email' in user)
            self.assertEqual(True, 'firstname' in user)
            self.assertEqual(True, 'lastname' in user)
            self.assertEqual(True, 'username' in user)

    def tearDown(self):
        # Follow.objects.get(followee_id=self.user1, follow_id=self.user2).delete()
        pass