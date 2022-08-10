from django.db import models
from user.models import User

from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class UserFollow(models.Model):
      # The one that follows
    source = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    # The one that is followed
    destination = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followee')
    # We never delete a follow relationship
    isFollowing = models.BooleanField(default=True)



    
    def getJson(self):
        json = {
            "id": self.id,
            "source": self.source.getJson(),
            "destination": self.destination.getJson(),
            "isFollowing": self.isFollowing,
            
        }
        return json


    def __str__(self) -> str:
        return f'''
        {self.id}\n
        {self.source}\n
        {self.destination}\n
        {self.isFollowing}\n
        '''