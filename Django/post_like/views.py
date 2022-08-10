from django.http import Http404, JsonResponse
from rest_framework import status
from rest_framework import generics

from user.views import getUserId
from user_post.models import UserPost
from .models import PostLike
from .serializers import PostLikeSerializer


class LikeAPIVIEW(generics.GenericAPIView):
    '''
    GET - get like status on 
    POST - 
    '''
    def __init__(self) -> None:
        self.serializer = PostLikeSerializer()
    



    ''' Liking a post with a postId '''
    def post(self, request, postId):
        # Get userId from request - bearer token
        userId = getUserId(request)
        
        data = {
            'user': userId,
            'post': postId,
        }

        # Create serializer instance with data from relevent to PostLike model
        serializer = PostLikeSerializer(data=data)

        # Have we validated our data?
        if serializer.is_valid():
            
            # Update Doeslike status of the instance or create new instance and store to db 
            data = serializer.update_or_create_PostLike()

            # Return data back to user
            return JsonResponse(data, status=status.HTTP_200_OK)
        


    def get(self, request, postId):
        ''' Check if the authenticated user already likes a post '''
        userId = getUserId(request)

        # All likes for a specific post - postId
        likes = PostLike.objects.filter(post_id=postId)

        likes = [x.getJson() for x in likes if x.doesLike]

        return JsonResponse({"likes": likes}, status=status.HTTP_200_OK)

# class LikeUsersAPIVIEW(generics.GenericAPIView):
#     def get(self,request,postId):
#         pass