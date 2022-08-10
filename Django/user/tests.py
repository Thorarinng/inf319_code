from .models import User
from django.test import TestCase, SimpleTestCase, Client


class UserTestCase(SimpleTestCase):
    databases = "__all__"

    def setUp(self):
        """
        Necessary definition that need to exist before running all the defined tests
        :return:
        """
        body = {
            "email": "test1@gmail.com",
            "password": "test1234",
            "password2": "test1234",
            "username": "test1",
            "firstname": "test12s",
            "lastname": "test12",
            "imgURL": "IMAGE_URL"
        }
        # necessary for tearDown() to work
        self.user = {"id": 0}

        # client-stub
        self.client = Client()

        # URI's tested
        self.login_uri = '/api/user/login/'
        self.register_uri = '/api/user/register/'
        self.logout_uri = '/api/user/logout/'
        self.update_uri = "/api/user/update/"

        user_res = self.client.post(self.register_uri, body)

    def test_login(self):
        body = {
            "email": "test1@gmail.com",
            "password": "test1234"
        }

        response = self.client.post(self.login_uri, body)
        user = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(True, 'email' in user)
        self.assertEqual(True, 'password' in user)
        self.assertEqual(True, 'password2' in user)
        self.assertEqual(True, 'firstname' in user)
        self.assertEqual(True, 'lastname' in user)
        self.assertEqual(True, 'username' in user)
        self.assertEqual(True, 'tokens' in user)
        self.assertEqual(True, 'refresh' in user['tokens'])
        self.assertEqual(True, 'access' in user['tokens'])
        return user

    def registerTest(self):
        body = {
            "email": "test12@gmail.com",
            "password": "test1234",
            "password2": "test1234",
            "username": "test12",
            "firstname": "test12s",
            "lastname": "test12",
            "imgURL": "IMAGE_URL"
        }

        user_res = self.client.post(self.register_uri, body)
        user = user_res.data
        self.user = user

        self.assertEqual(user_res.status_code, 201)
        self.assertEqual(True, 'email' in user)
        self.assertEqual(True, 'password' in user)
        self.assertEqual(True, 'password2' in user)
        self.assertEqual(True, 'firstname' in user)
        self.assertEqual(True, 'lastname' in user)
        self.assertEqual(True, 'username' in user)
        self.assertEqual(True, 'tokens' in user)
        self.assertEqual(True, 'refresh' in user['tokens'])
        self.assertEqual(True, 'access' in user['tokens'])

    def _test_logout(self, tokens):
        """
        Helper function that is not run like a test, however is called from a testing function test_register_login
        :param tokens:
        :return:
        """
        bearer_token = tokens['access']
        headers = {"Authorization": f"Bearer {bearer_token}"}

        user_res = self.client.post(
            self.logout_uri, HTTP_AUTHORIZATION=headers['Authorization'], data=tokens)

        self.assertEqual(user_res.status_code, 204)

    def test_register_login(self):
        """
        Tests login and login in one go
        :return:
        """
        self.registerTest()            # User needs exist
        # login to get data about user - this could be skipped since we are already registering and getting the same response.data
        user = self.test_login()

        # Run logout function to test logout functionality.
        self._test_logout(user['tokens'])

    def test_update(self):
        """
        Tests updating a user
        """
        # login to get information
        print("asdasd")
        user_res = self.client.post(self.login_uri, {"email": "test1@gmail.com",
                                                     "password": "test1234", })
        user = user_res.data

        body = {
            "email": "test1@gmail.com",
            "password": "test1234",
            "password2": "test1234",
            "username": "test1",
            "firstname": "test1",
            "lastname": "test1",
            "imgURL": "IMAGE_URL"
        }

        headers = {"Authorization": f"Bearer {user['tokens']['access']}"}

        user_res = self.client.patch(
            self.update_uri, body, HTTP_AUTHORIZATION=headers['Authorization'], content_type='application/json')

        self.assertEqual(user_res.status_code, 200)

        # New user object
        user = user_res.data['user']
        self.user = user

        actualUserRes = self.client.post(self.login_uri, {
            "email": "test1@gmail.com", "password": "test1234"}, HTTP_AUTHORIZATION=headers['Authorization'])

        actualUser = actualUserRes.data

        self.assertEqual(actualUser['id'], user['id'])
        self.assertEqual(actualUser['username'], user['username'])
        self.assertEqual(actualUser['email'], user['email'])
        self.assertEqual(actualUser['firstname'], user['firstname'])
        self.assertEqual(actualUser['lastname'], user['lastname'])

    def tearDown(self) -> None:
        """
        Cleanup after tests pass, removing the registered user.
        :return:
        """
        body = {"email": "test12@gmail.com",
                "password": "test1234", }

        try:
            user_res = self.client.post(self.login_uri, body)
            id = user_res.data['id']
            User.objects.filter(id=id).delete()
        except:
            pass
