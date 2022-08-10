from django.db import models
from user.models import User

# Create your models here.
from django.core.validators import MaxValueValidator, MinValueValidator
import time
import calendar

class UserPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    comment = models.CharField(max_length=255, default=None, null=True)
    likeCount = models.IntegerField(default=0)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, default=None, null=True)

    date = models.CharField(max_length=255)


    def __str__(self) -> str:
        return 'Post Instance: {' + f'{self.id}, ' \
               f'{self.user}, ' \
               f'{self.comment}, '\
               f'{self.likeCount}, ' \
               f'{self.parent}, ' \
               f'{self.date}, ' \
 \

    def getJson(self, getFullUserObj=False):
        if getFullUserObj:
            try:
                json = {
                    "id": self.id,
                    "user": self.user.getJson(),
                    "comment": self.comment,
                    "likeCount": self.likeCount,
                    "parent": self.parent.id,
                    "date": self.date,
                }
            except:
                json = {
                    "id": self.id,
                    "user": self.user.getJson(),
                    "comment": self.comment,
                    "likeCount": self.likeCount,
                    # None sometimes
                    "parent": self.parent,
                    "date": self.date,
                }
        else:
            try:
                json = {
                    "id": self.id,
                    "user": self.user.id,
                    "comment": self.comment,
                    "likeCount": self.likeCount,
                    "parent": self.parent.id,
                    "date": self.date,
                }
            except:
                json = {
                    "id": self.id,
                    "user": self.user.id,
                    "comment": self.comment,
                    "likeCount": self.likeCount,
                    # None sometimes
                    "parent": self.parent,
                    "date": self.date,
                }
        return json
