from django.db import models
from naive_user.models import User

from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Follow(models.Model):
    # The one that follows
    follows = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower')
    # The one that is followed
    followee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followee')
    # We never delete a follow relationship
    isFollowing = models.BooleanField(default=True)

    def getJson(self):
        json = {
            "id": self.id,
            "source": self.follows.getJson(),
            "destination": self.followee.getJson(),
            "isFollowing": self.isFollowing,
            
        }
        return json


    def __str__(self) -> str:
        return f'''
        {self.id}\n
        {self.follows}\n
        {self.followee}\n
        {self.isFollowing}\n
        '''