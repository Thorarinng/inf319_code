
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.http import JsonResponse

from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from naive_post.models import Post
from naive_likes.models import Likes
from naive_follow.models import Follow
from naive_user.models import User
from naive_user.views import getUserId



import time
import calendar



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


def evaluateCommentTags(post):
    a = post.comment.split("@")

    # remove the first element
    a = a[1:]

    usersFound = []
    for sentence in a:
        user = sentence.split(" ")
        b = user[0]
        u = User.objects.get(username=b)

        # Only notify the users once, regardless if he was tagged multiple times in the same postt
        if u not in usersFound:
            usersFound.append(u)

    return usersFound


def getPostLis(likes, posts, userId, user=None):
    '''Returns the postlist in the format displayable by the frontend adding whether or not
        the user has liked that specific post'''
    # Get post_ids of like objects
    likeIds = list(map(lambda x: x.post_id, likes))
    # Check if post_ids are in posts
    postsLiked = [post for post in posts if post.id in likeIds]
    # Set doesLike attr
    # convert to JSON serializable format
    postsList = []
    for post in posts:
        if post in postsLiked:
            post = post.getJson()
            post['doesLike'] = True
        else:
            post = post.getJson()
            post['doesLike'] = False
        if post["user"] != userId:
            userThatPosted = User.objects.get(id=post["user"])
            # User that owns post
            post['user'] = userThatPosted.getJson()
        else:
            # requestee owns post, no need to get his information since we already have it
            post['user'] = user.getJson()
        postsList.append(post)
    return postsList


class PostAPIVIEW(generics.GenericAPIView):
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
            return JsonResponse({"invalid": "Invalid comment"}, status=status.HTTP_400_BAD_REQUEST)
        # As long as we have a validated user and a valid comment we can post it
        post = Post(user=user, comment=comment, date=ts)
        # Save to database
        post.save()

        usersFound = evaluateCommentTags(post)

        thePost = post.getJson()
        return JsonResponse(thePost, status=status.HTTP_200_OK)

    def getDiscoverPosts(self, request):
        ''' Discover new posts'''
        postsList = []
        pFunc = PostAPIVIEW()
        userId = getUserId(request)
        likes = Likes.objects.filter(user_id=userId, doesLike=True)
        try:
            posts = Post.objects.filter(parent_id=None).order_by('-date')[:10]
            pFunc.posts = posts
            pFunc.likes = likes
            postsList = getPostLis(likes, posts, userId, )
        except:
            print('Did not find any posts for the user ')
        return JsonResponse({'posts': postsList}, status=status.HTTP_200_OK)

    def getPostLis(likes, posts, userId, user=None):
        '''Returns the postlist in the format displayable by the frontend adding whether or not
            the user has liked that specific post'''
        # Get post_ids of like objects
        likeIds = list(map(lambda x: x.post_id, likes))
        # Check if post_ids are in posts
        postsLiked = [post for post in posts if post.id in likeIds]
        # Set doesLike attr
        # convert to JSON serializable format
        postsList = []
        for post in posts:
            if post in postsLiked:
                post = post.getJson()
                post['doesLike'] = True
            else:
                post = post.getJson()
                post['doesLike'] = False
            if post["user"] != userId:
                userThatPosted = User.objects.get(id=post["user"])
                # User that owns post
                post['user'] = userThatPosted.getJson()

            else:
                # requestee owns post, no need to get his information since we already have it
                post['user'] = user.getJson()
            postsList.append(post)
        return postsList

    def get(self, request):
        ''' Get posts for the authenticated user '''
        self.userId = getUserId(request)
        print(self.userId)
        self.user = User.objects.get(id=self.userId)
        # Get your followers
        userFollowed = Follow.objects.filter(
            isFollowing=True, follows_id=self.userId)

        # Get myown and followers posts
        userFollowedId = [self.userId]
        for followee in userFollowed:
            userFollowedId.append(followee.followee.id)
        self.posts = Post.objects.filter(
            user_id__in=userFollowedId, parent_id=None).order_by('-date')
        self.likes = Likes.objects.filter(user_id=self.userId, doesLike=True)

        postLis = getPostLis(self.likes, self.posts, self.userId, self.user)

        if not postLis:
            pass
            # Here the user has no posts as they don't follow anyone or the people
            # They follow do not have any posts, so we grab posts on the website to
            # display to them

            # self.posts = Post.objects.filter(
            #     parent_id=None).order_by('-date')[:10]
            # self.likes = Likes.objects.filter(
            #     user_id=self.userId, doesLike=True)
            # # Getting posts in the right format with likes
            # postLis = getPostLis(self.likes, self.posts,
            #                      self.userId, self.user)

        return JsonResponse({'posts': postLis}, status=status.HTTP_200_OK)

    # Should completely remove the post from the database
    def delete(self, request, postId):
        ''' Delete a post '''
        userId = getUserId(request)
        try:
            # See if the post being deleted belongs to the authenticated user
            post = Post.objects.get(id=postId)
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
    def __init__(self):
        pass

    def post(self, request, postId):
        ''' Post a comment '''
        userId = getUserId(request)
        ts = getTime()
        try:
            # Check if the parent post exists
            post = Post.objects.get(id=postId)
            # Create a new post with original post as parent
            newPost = Post(user_id=userId, parent=post,
                           comment=request.data['comment'], date=ts)
            # At last save and then return
            newPost.save()
            # Grab a json version of the model
            jsonPost = newPost.getJson()

            usersFound = evaluateCommentTags(newPost)

        except:
            print("Could not create comment")
            # Return empty json so frontend knows how to react
            jsonPost = {}
        return JsonResponse(jsonPost, status=status.HTTP_200_OK)

    # Get all comments of a specific post
    def get(self, request, postId):
        postList = []
        posts = Post.objects.filter(parent_id=postId)
        for post in posts:
            postJson = post.getJson(True)
            postList.append(postJson)
        return JsonResponse({"childrenPosts": postList}, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
class PostOtherAPIVIEW(generics.GenericAPIView):
    def get(self, request, username):
        postLis = []
        try:
            # Check if user exists
            user = User.objects.get(username=username)
            # Check if user has any posts
            posts = Post.objects.filter(user_id=user.id)
            # loop through all of them and change it from Django object to json object
            for post in posts:
                postLis.append(post.getJson())
        except:
            print('Did not find any posts for the user ')
        return JsonResponse({'posts': postLis}, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
class DiscoverPostAPIVIEW(generics.GenericAPIView):
    def get(self, request):
        ''' Returns 10 newest posts on the website'''
        postsList = []
        pFunc = PostAPIVIEW()
        try:
            posts = Post.objects.filter(parent_id=None).order_by('-date')[:10]
            pFunc.posts = posts
            postsList = pFunc.getPostLis()
        except:
            print('Did not find any posts for the user ')
        return JsonResponse({'posts': postsList}, status=status.HTTP_200_OK)
