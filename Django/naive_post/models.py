from django.db import models
from naive_user.models import User
# rom post.models import Post



class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    comment = models.CharField(max_length=255, default=None, null=True)
    likeCount = models.IntegerField(default=0)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, default=None, null=True)

    date = models.CharField(max_length=255)

    def __setPrivacyAttributes__(self, data):
        self.user = data['user']
        self.comment = data['comment']
        self.date = data['date']

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
