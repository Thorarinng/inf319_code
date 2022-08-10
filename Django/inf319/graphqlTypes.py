import graphene
from graphene_django import DjangoObjectType
from graphene import Field, String, Int, List

from user_follow.models import UserFollow
from user_post.models import UserPost
from post_like.models import PostLike
from user.models import User


class PostLikeType(DjangoObjectType):
    class Meta:
        model = PostLike
        fields = ("id", "user", "post", "doesLike")
 
class UserPostType(DjangoObjectType):
    # Connect model = userPost metadata to the UerPostType - with an extra field likes as PostLikeType

    # Likes for the corresponding post
    likes = Field(List(PostLikeType))
    
    # Connect model = userPost metadata to the UerPostType
    class Meta:
        model = UserPost
        fields = ("id","user", "comment", "likeCount", "parent", "date", "doesLike")

    # Get the likes for the specific post
    def resolve_likes(root,info):
        return PostLike.objects.filter(post_id=root.id)

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id","email", "username", "firstname", "lastname", "imgURL", "date")


    def __str__(self):
        return f'''
        {self.id}\n
        {self.email}\n
        {self.username}\n
        {self.firstname}\n
        {self.lastname}\n
        {self.imgURL}\n
        {self.date}\n
        '''

class UserFollowType(DjangoObjectType):
    id = Int(source='pk')
    class Meta:
        model = UserFollow
        fields = ("id", "source", "destination", "isFollowing")

    def __str__(self):
        return f'''
        {self.id}\n
        {self.source}\n
        {self.destination}\n
        {self.isFollowing}\n
        '''
