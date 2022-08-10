from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from naive_user.models import User
from naive_user.views import getUserId
from naive_follow.models import Follow

from random import randint
from django.db.models import Q
# Create your views here.


class FollowAPIVIEW(generics.GenericAPIView):
    def __init__(self):
        self.userId = -1
        self.serializer = None


    # Returns true if user follows the person with that username

    def get(self, request, username):
        # Extract user ID from the request authorization headers
        self.userId = getUserId(request)
        user = User.objects.get(username=username)
        fol = {
            "isFollowing": False
        }
        try:
            relationship = Follow.objects.get(
                follows=self.userId, followee=user.id)
            # We find the relationship, does not the user follows them, but that they have at some point followed them
            fol = {
                # assign whatever isFollowing is (could be either True or False)
                "isFollowing": relationship.isFollowing
            }
        except:
            # Returns "isFollowing" : False, not a bad request so we return 200_OK
            print("Does not follow user ")
        return Response(fol, status=status.HTTP_200_OK)

    def post(self, request, username):
        # This should never crash, Django REST handles authentication issues
        self.userId = getUserId(request)
        # Get user instance
        follower = User.objects.get(id=self.userId)
        try:
            # Does the user exist
            # Get user instance
            followee = User.objects.get(username=username)

            # Cant follow yourself
            if (followee.id == self.userId):
                return Response({"isFollowing": False}, status=status.HTTP_200_OK)
        except:
            print("Follower not found")
            return Response({"isFollowing": False}, status=status.HTTP_400_BAD_REQUEST)
        try:

            # Get if they have a relationship
            relationship = Follow.objects.get(
                follows=follower, followee=followee)

            # Flip the status if they exist
            relationship.isFollowing = not relationship.isFollowing
            # Save it
            relationship.save()
        except:
            # Create a new relationship inside Follow table
            relationship = Follow(follows=follower,
                                  followee=followee)
            relationship.save()


        return Response({"isFollowing": relationship.isFollowing}, status=status.HTTP_200_OK)

class FollowersAPIVIEW(generics.GenericAPIView):
    def get(self,request):
        userId = getUserId(request)

        followers = Follow.objects.filter(follows=userId, isFollowing=True)

        followers = [x.getJson() for x in followers]

        return Response({"followers": followers},status=status.HTTP_200_OK)




class FollowingAPIVIEW(generics.GenericAPIView):
    def get(self,request):
        userId = getUserId(request)

        following = Follow.objects.filter(followee=userId, isFollowing=True)

        following = [x.getJson() for x in following]
        
        return Response({"following": following},status=status.HTTP_200_OK)