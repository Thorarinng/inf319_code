from django.db import models
from user.models import User
from user_post.models import UserPost
# Create your models here.


class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    doesLike = models.BooleanField(default=True)


    def __str__(self) -> str:
        return super().__str__()

    def __str__(self) -> str:
        return 'postLike Instance: {' + f'{self.id}, ' \
               f'{self.user}, ' \
               f'{self.post}, '\
               f'{self.doesLike}, ' \
    
    def getJson(self):
        json = {
            "user": self.user.id,
            "post": self.post.id,
            "doesLike": self.doesLike,
        }
        return json