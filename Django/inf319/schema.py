
   
import graphene
from graphene import Field, List
from post_like.models import PostLike
from user_follow.models import UserFollow
from user_post.models import UserPost
from user.models import User
from user.views import getUserId
from post_like.models import PostLike
from user_follow.models import UserFollow

from .redisService import RedisService
redis_service = RedisService()

from .graphqlTypes import UserFollowType, UserPostType, UserType

import json

def getUserPosts(ufs_ids):
    # Get all posts corresponding to the ids in ufs_ids

    up1 = UserPost.objects.filter(user_id__in=ufs_ids)


    return up1

def getUserFollows(destinationId):
    # Everyone that destinationId (userId) follows
    # TODO: Cache UserFollow list
    ufs = UserFollow.objects.filter(destination=destinationId, isFollowing=True)


    # Create a list of userIds
    ufs_ids = [x.source.id for x in ufs]
    # Add your own userId 
    ufs_ids.append(destinationId)

    return ufs_ids

class AllPostType(graphene.ObjectType):
    posts = Field(List(UserPostType))

    def resolve_likes(root,info):
        return PostLike.objects.all()

    def resolve_posts(root,info):
        '''
        User has access to their own posts and the posts of their followers
        1. Followers list is fetched 
        2. Posts corrresponding to the users followers and the user himself are fetched
        3. A list of UserPosts is returned
        '''

        # Retrieve userId from the JWT-Bearer token
        userId = getUserId(info.context)
        destinationId = userId

        key = f"following-{userId}"



        # UserFollowsIds - Ids of all the users they follow
        # ufs_ids = getUserFollows(destinationId)

        ufs_ids = redis_service.redis_and_db(key,userId,isFollowing=False)

        # Get all posts corresponding to the ids in ufs_ids
        up = getUserPosts(ufs_ids)

        return up


class AllUserFollowType(graphene.ObjectType):

    followers = Field(List(UserFollowType))
    following = Field(List(UserFollowType))


    def resolve_followers(root,info):
        ''' 
        '''
        # TODO: Redis implementation
        userId = getUserId(info.context)

        key = f"followers-{userId}"
        
        return redis_service.redis_and_db(key,userId,isFollowing=False)

    def resolve_following(root,info):
        # TODO: Redis implementation
        userId = getUserId(info.context)

        key = f"following-{userId}"

        return redis_service.redis_and_db(key,userId,isFollowing=True)

        

class Query(graphene.ObjectType):

    all_posts = Field(AllPostType)
    all_followers = Field(AllUserFollowType)

    def resolve_all_posts(root,info):
        '''
        User has access to their own posts and the posts of their followers
        1. Followers list is fetched 
        2. Posts corrresponding to the users followers and the user himself are fetched
        3. A list of UserPosts is returned
        '''
        
        # TODO This is commented out to enable caching-protocol
        # redis_service.redis.flushdb()

        return AllPostType()

    def resolve_all_followers(root,info):
        return AllUserFollowType()



schema = graphene.Schema(query=Query)