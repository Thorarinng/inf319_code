from django.test import TestCase

# Create your tests here.

from django.test import TestCase, SimpleTestCase, Client
from user.models import User
from post.models import Post
from follow.models import Follow
import os
import json
# Create your tests here.

# TESTING STUFF
# https://docs.djangoproject.com/en/3.1/topics/testing/tools/


class PostTestCase(SimpleTestCase):
    databases = "__all__"

    def setUp(self):
        # Used to run tests
        self.client = Client()
        # Login uri
        self.login_uri = '/api/user/login/'
        self.followUser = '/api/follow/'
        self.user = {}
        self.response = {}
        self.bearer_token = ''
        self.headers1 = ''
        self.headers2 = ''
        self.tokens = ''
        self._setupUsers()

        # Get posts of followers
        self.post_uri = "/api/post/"
        self.get_post_uri = "/api/post/start/0/end/100"
        self.createComment_uri = "/api/post/comment/"

    # FOllow user test
    # Example of call: http://localhost:8000/api/follow/totisg/

    def serialize_json(self, res):
        return json.loads(res.content.decode("utf-8"))

    def genToken(self, response):
        user = response.data
        self.tokens = user['tokens']
        self.bearer_token = self.tokens['access']
        return {"Authorization": f"Bearer {self.bearer_token}"}

    def _setupUsers(self):
        body1 = {
            "email": "test1@gmail.com",
            "password": "test1234",
        }
        body2 = {
            "email": "test2@gmail.com",
            "password": "test1234",
        }

        # Login
        res1 = self.client.post(self.login_uri, body1)
        res2 = self.client.post(self.login_uri, body2)

        # Set auth header
        self.headers1 = self.genToken(res1)
        self.headers2 = self.genToken(res2)

        # Set user instances
        self.user1 = res1.data
        self.user2 = res2.data

    def userInPost(self, expUser, actUser):
        # Expected user and actual user
        self.assertEqual(True, 'email' in expUser)
        self.assertEqual(False, 'password' in expUser)
        self.assertEqual(False, 'password2' in expUser)
        self.assertEqual(True, 'firstname' in expUser)
        self.assertEqual(True, 'lastname' in expUser)
        self.assertEqual(True, 'username' in expUser)

        self.assertEqual(expUser['username'], actUser['username'])
        self.assertEqual(expUser['email'], actUser['email'])
        self.assertEqual(expUser['firstname'], actUser['firstname'])
        self.assertEqual(expUser['lastname'], actUser['lastname'])

    def getPosts(self):
        res = self.client.get(
            self.get_post_uri, HTTP_AUTHORIZATION=self.headers1["Authorization"])

        posts = self.serialize_json(res)['posts']

        self.assertEqual(res.status_code, 200)

        for post in posts:
            self.assertEqual(type(post['id']), int)
            self.assertGreater(len(post['comment']), 0)
            self.assertEqual(post['likeCount'], 0)
            self.assertEqual(post['parent'], None)
            self.assertGreater(int(post['date']), 0)
            # Check if user information is there
            self.assertEqual(type(post['user']), dict)
            self.userInPost(post['user'], self.user1)

        return posts

    def createPost(self):
        comment = "This is a test"
        res = self.client.post(
            self.post_uri, {"comment": comment}, HTTP_AUTHORIZATION=self.headers1["Authorization"])
        post = self.serialize_json(res)

        self.assertEqual(res.status_code, 200)

        self.assertEqual(type(post['id']), int)
        self.assertEqual(post['user'], self.user1['id'])
        self.assertEqual(post['comment'], comment)
        self.assertEqual(post['likeCount'], 0)
        self.assertEqual(post['parent'], None)
        self.assertGreater(post['date'], 0)

        self.getPosts()

        return post

    def test_post_posts(self):
        """
        create a post
        """
        self.createPost()

    def test_get_posts(self):
        """
        get your own posts
        """
        self.createPost()
        self.getPosts()

    def test_delete_posts(self):
        """
        delete a specific post
        """
        # Create post
        post = self.createPost()
        postId = post['id']

        # get post
        uri = self.get_post_uri
        res = self.client.get(
            uri, HTTP_AUTHORIZATION=self.headers1["Authorization"])

        # Filter through posts and make sure there exists a post with the specific id
        posts = self.serialize_json(res)['posts']
        post = [ep for ep in posts if ep['id'] == post['id']]
        self.assertEqual(len(post), 1)
        self.assertEqual(res.status_code, 200)

        # Delete post
        uri = self.post_uri + str(postId) + "/"
        res = self.client.delete(
            uri, HTTP_AUTHORIZATION=self.headers1["Authorization"])

        # get post
        uri = self.get_post_uri
        res = self.client.get(
            uri, HTTP_AUTHORIZATION=self.headers1["Authorization"])

        # Filter through posts and make sure the post with the specific id is DELETED
        posts = self.serialize_json(res)['posts']
        post = [ep for ep in posts if ep['id'] == post[0]['id']]
        self.assertEqual(len(post), 0)

    def createComment(self, post):
        comment = {'comment': "This is a test comment"}
        uri = self.createComment_uri + str(post['id']) + "/"
        res = self.client.post(
            uri, comment, HTTP_AUTHORIZATION=self.headers1["Authorization"])

        # Status code
        self.assertEqual(res.status_code, 200)

        c = self.serialize_json(res)

        return c, comment

    def test_post_comment_posts(self):
        """
        post comment to a specific post
        """
        post = self.createPost()
        c, cStr = self.createComment(post)

        # res has following
        self.assertEqual(True, "id" in c)
        self.assertEqual(True, "user" in c)
        self.assertEqual(True, "comment" in c)
        self.assertEqual(True, "likeCount" in c)
        self.assertEqual(True, "parent" in c)
        self.assertEqual(True, "date" in c)

        # values
        self.assertEqual(c['user'], self.user1['id'])
        self.assertEqual(c['comment'], cStr['comment'])
        self.assertEqual(c['likeCount'], 0)
        self.assertEqual(c['parent'], post['id'])
        self.assertEqual(type(c['date']), int)

    def getComments(self, p):
        res = self.client.get(self.createComment_uri + str(p['id']) + "/")
        cs = self.serialize_json(res)['childrenPosts']

        return cs

    def test_get_comment_posts(self):
        """
        get comments belonging to a specific post
        """
        p = self.createPost()
        c = self.createComment(p)

        cs = self.getComments(p)

        for c in cs:

            self.assertEqual(True, 'id' in c)
            self.assertEqual(c['user']['id'], self.user1['id'])
            self.assertGreater(len(c['comment']), 0)
            self.assertEqual(c['likeCount'], 0)
            self.assertEqual(c['parent'], p['id'])
            self.assertGreater(len(c['date']), 0)

    def user2HasNoPostsAvail(self, pAmount):
        # posts user2 can see
        res = self.client.get(
            self.get_post_uri, HTTP_AUTHORIZATION=self.headers2["Authorization"])
        ps = self.serialize_json(res)['posts']
        # user2 can see no posts, he owns no posts and is not following anyone with posts
        self.assertEqual(len(ps), pAmount)

    def test_see_others_posts(self):
        """
        Tests if posts of people you follow show up
        """

        # posts user2 can see
        # top 10 newest posts because he has 0 followers
        pAmount = 0
        self.user2HasNoPostsAvail(pAmount)

        # user1 creates a post
        self.createPost()

        # posts user2 still can't see posts
        pAmount = 0
        self.user2HasNoPostsAvail(pAmount)

        # Now user2 follows user1
        uri = "/api/follow"
        res = self.client.post(
            f'{self.followUser}{self.user1["username"]}/', HTTP_AUTHORIZATION=self.headers2["Authorization"])

        # Now follow user and make sure it returns correctly
        pAmount = 1
        self.user2HasNoPostsAvail(pAmount)

    def tearDown(self) -> None:
        """
        For each test entries are created in Portfolio and Transactions tables
        This function handles removing those values again out from the database
        """
        id = self.user1['id']
        Post.objects.filter(user_id=id).delete()
        Follow.objects.filter(followee_id=id).delete()
