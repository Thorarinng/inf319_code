from django.http import JsonResponse
from rest_framework import status
from rest_framework import generics

from naive_likes.models import Likes
from user.views import getUserId
from naive_post.views import Post



class LikesAPIVIEW(generics.GenericAPIView):
    def __init__(self):
        pass
    ''' Liking a post with a postId '''

    def post(self, request, postId):
        userId = getUserId(request)
        toReturn = {}
        try:
            # Parent
            print("before getting post")
            post = Post.objects.get(id=postId)
            print("Founds post ", post)
            # Lets find the children of parent
            try:
                # Should be one like here - we get list back
                likes = Likes.objects.filter(post_id=post.id, user_id=userId)
                # Has a record of liking the post - true/false
                # Flip the boolean
                print(likes)
                if len(likes) == 0:
                    like = Likes(post_id=postId, user_id=userId)
                    like.save()
                    toReturn = like.getJson()
                else:
                    for like in likes:
                        like.doesLike = not like.doesLike
                        like.save()
                        toReturn = like.getJson()
            except:
                pass
            # increment and decrement like count
            if like.doesLike:
                post.likeCount += 1
                # Send a broadcast to a user that a user liked their post
                self.notificationsService.createLikeNotification(like)
            else:
                post.likeCount -= 1
            post.save()
        except:
            print("Could not like post ")
            return JsonResponse({'post': 'Could not like post'}, status=status.HTTP_400_BAD_REQUEST)
        toReturn['likeCount'] = post.likeCount
        return JsonResponse({'post': toReturn}, status=status.HTTP_200_OK)

    def get(self, request, postId):
        ''' Check if the authenticated user already likes a post '''
        userId = getUserId(request)
        # Get all posts belonging to a certain postId=parent_id
        # and return the length of the of the list
        childrenOfPost = Likes.objects.filter(post_id=postId, doesLike=True)
        toReturn = {"postCount": len(childrenOfPost), "like": False}

        for child in childrenOfPost:
            if child.user_id == userId:
                toReturn['like'] = child.doesLike
                break

        return JsonResponse(toReturn, status=status.HTTP_200_OK)
