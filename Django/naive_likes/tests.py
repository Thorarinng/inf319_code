from django.test import TestCase

# Create your tests here.

from django.test import TestCase, SimpleTestCase, Client
from user.models import User
from post.models import Post
from follow.models import Follow
from likes.models import Likes
import os
import json
# Create your tests here.

# TESTING STUFF
# https://docs.djangoproject.com/en/3.1/topics/testing/tools/


class PrivacyTestCase(SimpleTestCase):
    databases = "__all__"

    def setUp(self):
        # Used to run tests
        self.client = Client()
        # Login uri
        self.login_uri = '/api/user/login/'
        self.followUser = '/api/follow/testuser2/'
        self.register_uri = '/api/user/register/'
        self.buyEquityUrl = '/api/transactions/'
        self.like_url = '/api/likes/'
        self.user = {}
        self.response = {}
        self.bearer_token = ''
        self.headers1 = ''
        self.headers2 = ''
        self.tokens = ''
        self._setupUsers()
        # This is a test user that owns certain standardEquity
        self.testUser3 = '/api/follow/testuser3/'

        # Get posts of followers
        self.postOfFollowers_uri = '/api/post/'
        self.createPost_uri = "/api/post/"
        self.deletePost_uri = "/api/delete/"
        self.createComment_uri = "/api/post/comment/"

        self.uriGetFollowersOfEquitySuccessCase = '/api/follow/equity/fb/'
        self.uriGetFollowersOfEquityFailCase = '/api/follow/equity/gme/'

        self.postId = 0
    # FOllow user test
    # Example of call: http://localhost:8000/api/follow/totisg/

    def serialize_json(self, res):
        print("---------serialize json-----------------")
        print(res.content)
        try:
            try:
                d = json.loads(res.content.decode("utf-8"))['posts']
            except:
                d = json.loads(res.content.decode("utf-8"))
        except:
            print("crash")
        return d

    def genToken(self, response):
        # print("Logging response ", response)
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

    def createPost(self):
        comment = "This is a test"
        res = self.client.post(
            self.createPost_uri, {"comment": comment}, HTTP_AUTHORIZATION=self.headers1["Authorization"])
        print("------- created post -------")
        post = self.serialize_json(res)

        self.assertEqual(res.status_code, 200)

        self.assertEqual(type(post['id']), int)
        self.assertEqual(post['user'], self.user1['id'])
        self.assertEqual(post['comment'], comment)
        return post

    #
    #
    def test_like_post(self):
        post = self.createPost()
        self.postId = post['id']
        print("Logging post ", post)
        print("User 1 ", self.user1['id'])
        print("User 2 ", self.user2['id'])
        comment_url = '/api/post/comment/' + str(post['id']) + '/'
        commentBody = {
            "comment": "Commentiquette"
        }
        # Now user 2 wants to post a comment on that post
        comment = self.client.post(
            comment_url, commentBody, HTTP_AUTHORIZATION=self.headers1["Authorization"])
        d = self.serialize_json(comment)
        print("The comment posted ", d)
        self.assertEqual(d['comment'], 'Commentiquette')
        print("Post req ", self.like_url + str(self.postId) + '/')
        # Check if the comment
        like = self.client.post(self.like_url + str(self.postId) +
                                '/', HTTP_AUTHORIZATION=self.headers1["Authorization"])
        print("Like response ", like)
        # The post should have 1 like
        likedPost = Post.objects.get(id=self.postId)
        self.assertEqual(1, likedPost.likeCount)
        self.client.post(self.like_url + str(self.postId) + '/',
                         HTTP_AUTHORIZATION=self.headers2["Authorization"])
        # Now the post should have 2 likes
        likedPost = Post.objects.get(id=self.postId)
        self.assertEqual(2, likedPost.likeCount)

        # Unlike a post
        self.client.post(self.like_url + str(self.postId) + '/',
                         HTTP_AUTHORIZATION=self.headers2["Authorization"])
        likedPost = Post.objects.get(id=self.postId)
        self.assertEqual(1, likedPost.likeCount)

        # Relike a post
        self.client.post(self.like_url + str(self.postId) + '/',
                         HTTP_AUTHORIZATION=self.headers2["Authorization"])
        likedPost = Post.objects.get(id=self.postId)
        self.assertEqual(2, likedPost.likeCount)

    def test_like_body(self):
        post = self.createPost()
        comment_url = '/api/post/comment/' + str(post['id']) + '/'
        commentBody = {
            "comment": "Commentiquette"
        }
        # Now user 2 wants to post a comment on that post
        comment = self.client.post(
            comment_url, commentBody, HTTP_AUTHORIZATION=self.headers1["Authorization"])
        d = self.serialize_json(comment)
        self.assertEqual(d['comment'], 'Commentiquette')
        # Check if the comment
        like = self.client.post(
            self.like_url + str(post['id']) + '/', HTTP_AUTHORIZATION=self.headers1["Authorization"])
        d = self.serialize_json(like)

        self.assertEqual(True, 'doesLike' in d['post'])
        self.assertEqual(False, 'post_id' in d['post'])
        self.assertEqual(False, 'user_id' in d['post'])

    def tearDown(self):
        """
        For each test entries are created in Portfolio and Transactions tables
        This function handles removing those values again out from the database
        """
        id = self.user1['id']
        Post.objects.filter(user_id=id).delete()
        Follow.objects.filter(followee_id=id).delete()
        Likes.objects.filter(post_id=self.postId).delete()
