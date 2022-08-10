
from django.http import JsonResponse
from rest_framework import status
from rest_framework import generics
from user_post.models import *
from post_like.models import PostLike
from user_follow.models import UserFollow
from user_follow.models import *
from post_like.models import PostLike
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.core import serializers
import json as json

import time
import calendar
from user.views import getUserId

def getTime():
    ''' Gets the current time (gmt) '''
    gmt = time.gmtime()
    ts = calendar.timegm(gmt)
    return ts
def isCommentValid(comment):
    ''' Checks the validity of a comment (type, length)'''
    # Check type of comment
    if type(comment) != str:
        return False
    elif len(comment) < 0:
        return False
    elif len(comment) > 256:
        return False
    return True

class PostAPIVIEW(generics.GenericAPIView):
    '''
    GET - Gets posts for a specific user
    POST - creates a post registered to a specific user given input connected to the post
    DELETE - Removes the post from the database
    '''
    def __init__(self):
        self.serializer = None
        self.userId = 0
        self.posts = ''
        self.likes = ''
        self.user = {}
    # Creating a normal post
    def post(self, request):
        ''' Creates a new post '''
        # Getting userId from token
        userId = getUserId(request)
        user = User.objects.get(id=userId)
        ts = getTime()
        comment = request.data['comment']
        if not isCommentValid(comment):
            return JsonResponse({"invalid":"Invalid comment"}, status=status.HTTP_400_BAD_REQUEST)
        # As long as we have a validated user and a valid comment we can post it
        post = UserPost(user=user, comment=comment, date=ts)
        # Save to database
        post.save()
        thePost = post.getJson()
        return JsonResponse(thePost, status=status.HTTP_200_OK)

    def getPostLis(self):
        '''Returns the postlist in the format displayable by the frontend adding whether or not
            the user has liked that specific post'''
        # Get post_ids of like objects
        likeIds = list(map(lambda x: x.post_id, self.likes))
        # Check if post_ids are in posts
        postsLiked = [post for post in self.posts if post.id in likeIds]
        # Set doesLike attr
        # convert to JSON serializable format
        postsList = []
        for post in self.posts:
            if post in postsLiked:
                post = post.getJson()
                post['doesLike'] = True
            else:
                post = post.getJson()
                post['doesLike'] = False
            if post["user"] != self.userId:
                userThatPosted = User.objects.get(id=post["user"])
                # User that owns post
                post['user'] = userThatPosted.getJson()
            else:
                # requestee owns post, no need to get his information since we already have it
                post['user'] = self.user.getJson()
            postsList.append(post)
        return postsList

    def getPostById(self,postId):
        # print(request)
        try:
            up = UserPost.objects.get(pk=postId)
            # up.user =  User.objects.get(id=up.user)
            return JsonResponse({"post": up.getJson(getFullUserObj=True)}, status=status.HTTP_200_OK)
        except UserPost.DoesNotExist:
            return JsonResponse({"err": f"Post with {postId} does not exist "}, status=status.HTTP_200_OK)

    def get(self, request):
        ''' Get posts for the authenticated user '''
        self.userId = getUserId(request)
        self.user = User.objects.get(id=self.userId)

        print(self.userId)
        
        # Get user's followers
        userFollowed = UserFollow.objects.filter(
            isFollowing=True, destination=self.userId)


        # Get myown and followers posts
        userFollowedId = [self.userId]



        for follow in userFollowed:
            userFollowedId.append(follow.source.id)

        self.posts = UserPost.objects.filter(
            user_id__in=userFollowedId, parent_id=None)


        self.posts = [x.getJson() for x in self.posts]


        # self.likes = PostLike.objects.filter(user_id=self.userId, doesLike=True)
        # postLis = self.getPostLis()

        # if not postLis:
        #     # Here the user has no posts as they don't follow anyone or the people
        #     # They follow do not have any posts, so we grab posts on the website to
        #     # display to them
        #     self.posts = UserPost.objects.filter(
        #         parent_id=None).order_by('-date')[:10]
        #     self.likes = PostLike.objects.filter(
        #         user_id=self.userId, doesLike=True)
        #     # Getting posts in the right format with likes
        #     postLis = self.getPostLis()
        return JsonResponse({'posts': self.posts}, status=status.HTTP_200_OK)

    # Should completely remove the post from the database
    def delete(self, request, postId):
        print(postId)
        ''' Delete a post '''
        userId = getUserId(request)
        try:
            # See if the post being deleted belongs to the authenticated user
            post = UserPost.objects.get(id=postId)
            if post.user_id == userId:
                # delete the post
                post.delete()
            else:
                return JsonResponse({'posts': 'This post does not belong to the user'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            # The post either does not exist or cannot be deleted
            print("Post not found")
            return JsonResponse({'posts': 'Post unable to be deleted'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'posts': 'Post deleted'}, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
class PostCommentAPIVIEW(generics.GenericAPIView):
    '''
    GET - Gets comments for a specific post <PostId>
    POST - Creates a comment for a post <PostId>
    '''
    def post(self, request, postId):
        ''' Post a comment '''
        userId = getUserId(request)
        ts = getTime()
        try:
            # Check if the parent post exists
            post = UserPost.objects.get(id=postId)
            # Create a new post with original post as parent
            newPost = UserPost(user_id=userId, parent=post,
                           comment=request.data['comment'], date=ts)
            # At last save and then return
            newPost.save()
            # Grab a json version of the model
            jsonPost = newPost.getJson()
        except:
            print("Could not create comment")
            # Return empty json so frontend knows how to react
            jsonPost = {}
        return JsonResponse(jsonPost, status=status.HTTP_200_OK)

    # Get all comments of a specific post
    def get(self, request, postId):
        postList = []
        posts = UserPost.objects.filter(parent_id=postId)
        for post in posts:
            postJson = post.getJson(True)
            postList.append(postJson)
        return JsonResponse({"childrenPosts": postList}, status=status.HTTP_200_OK)

@permission_classes([AllowAny])
class PostOtherAPIVIEW(generics.GenericAPIView):
    '''
    GET - Gets posts created by a specific user given a username
    '''
    def get(self, request, username):
        postLis = []
        try:
            # Check if user exists
            user = User.objects.get(username=username)
            # Check if user has any posts
            posts = UserPost.objects.filter(user_id=user.id)
            # loop through all of them and change it from Django object to json object
            for post in posts:
                postLis.append(post.getJson())
        except:
            print('Did not find any posts for the user ')
        return JsonResponse({'posts': postLis}, status=status.HTTP_200_OK)