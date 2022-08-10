from ast import Pass
from user_post.models import UserPost
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import PostLike
from django.contrib.auth import authenticate


class PostLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostLike
        fields = ['user', 'post', 'doesLike']
        extra_kwargs = {
            'password': {'error_messages': {'miss-match': "Passwords do not match"}},
        }


    def update_or_create_PostLike(self):
        user = self.validated_data['user']
        post = self.validated_data['post']

        up = UserPost.objects.get(id=post.id)

        try:
            pl = PostLike.objects.get(post_id=post.id, user_id=user.id)
            # Flip the relationship
            pl.doesLike = not pl.doesLike



            pl.save()
        except PostLike.DoesNotExist:
            # doesLike defaults to True
            pl = PostLike(post=post,user=user)

            # Store to db
            pl.save()



        # Return to user
        return pl.getJson()

    def validate(self, attrs):
        user = attrs.get('user', '')
        post = attrs.get('post', '')
        doesLike = attrs.get('doesLike', '')

        return {
            'user': user,
            'post': post,
            'doesLike': doesLike
        }
