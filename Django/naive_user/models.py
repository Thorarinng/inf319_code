# Django libraries
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models import Model

from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):

    def create_user(self, data):
        if not data['email']:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(data['email']),
            password=data['password'],
            username=data['username'],
            firstname=data['firstname'],
            lastname=data['lastname'],
            imgURL=data['imgURL'],
        )
        user.set_password(data['password'])
        user.save(using=self._db)

        return user

# User


class User(AbstractBaseUser):
    # In AbstractBaseUser : id, password, last_login
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    password2 = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    imgURL = models.CharField(max_length=999, blank=True)
    active = models.BooleanField(default=True)
    employee = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = [firstName, lastName, email]
    #
    objects = UserManager()
    #

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def __setUserAttributes__(self, data):
        self.email = data['email']
        self.set_password(data['password'])
        self.username = data['username']
        self.firstname = data['firstname']
        self.lastname = data['lastname']
        self.imgURL = data['imgURL']
        self.date = data['date']
    #

    def getJson(self):
        json = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "imgURL": self.imgURL,
            "firstname": self.firstname,
            "lastname": self.lastname
        }
        return json

    def __str__(self):
        return 'User Instance: {' + f'{self.id}, ' \
               f'{self.email}, ' \
               f'{self.password}, '\
               f'{self.username}, ' \
               f'{self.firstname}, ' \
               f'{self.lastname}, ' \
               f'{self.imgURL}, ' + '}' \
 \
            #
