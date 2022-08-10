from django.db import models
from user.models import User
from naive_post.models import Post
# Create your models here.


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    doesLike = models.BooleanField(default=True)
    def getJson(self):
        json = {
            "user": self.user.id,
            "post": self.post.id,
            "doesLike": self.doesLike,
        }
        return json