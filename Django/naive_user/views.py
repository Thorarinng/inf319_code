from .models import User
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework.authentication import get_authorization_header
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from .serializers import LoginSerializer, LogOutSerializer, RegisterSerializer, UpdateProfileSerializer
import jwt

from rest_framework import serializers

def getUserId(request):
    ''' Takes in the HTTP request and extracts the token out of it'''
    auth = get_authorization_header(request).split()
    decoded = jwt.decode(auth[1].decode("utf-8"), settings.SECRET_KEY, algorithms=['HS256'])
    return decoded['user_id']



@permission_classes([AllowAny])
class RegisterAPIVIEW(generics.GenericAPIView):
    def __init__(self):
        self.serializer_class = RegisterSerializer
        self.serializer = None

    def post(self, request):
        ''' Creates a new user '''
        self.serializer = self.serializer_class(data=request.data)
        self.serializer.is_valid(raise_exception=True)
        
        # Grab the newly created user
        user = User.objects.get(email=request.data['email'])


        return Response(self.serializer.validated_data, status=status.HTTP_201_CREATED)


@permission_classes([AllowAny])
class LoginAPIVIEW(generics.GenericAPIView):
    def __init__(self):
        self.serializer_class = LoginSerializer
        self.serializer = None

    def post(self, request):
        ''' Login to an account '''
        self.serializer = self.serializer_class(data=request.data)
        self.serializer.is_valid(raise_exception=True)
        user = User.objects.get(id=self.serializer.validated_data['id'])
        
        if not user.active:
            return Response({"detail": "User has been deleted"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(self.serializer.validated_data, status=status.HTTP_200_OK)

    def get(self, request):
        self.serializer = self.serializer_class(data=request.data)
        self.serializer.is_valid()
        return Response(request.header)


class LogOutAPIVIEW(generics.GenericAPIView):
    def __init__(self):
        self.serializer_class = LogOutSerializer
        self.serializer = None

    def post(self, request):
        ''' Logout from a session'''
        refresh = request.data['refresh']
        RefreshToken(refresh).blacklist()   # blacklists the refresh token
        return Response('', status=status.HTTP_204_NO_CONTENT)



def checkPassword(password, password2):
    # if len(password) < 6:
    #     raise serializers.ValidationError({'password': 'password too short'})
    if password != password2:
        raise serializers.ValidationError({'password': 'passwords not the same'})

def checkUsernameExists(username, userId):
    try:
        user = User.objects.get(username = username)
        if user.id != userId:
            return False
        else:
            return True
    except:
        return True


class UpdateProfile(generics.GenericAPIView):
    def __init__(self):
        self.serializer_class = UpdateProfileSerializer
        self.serializer = None

    def patch(self, request):
        ''' Update the profile of an authenticated user'''
        userId = getUserId(request)
        data = request.data
        user = User.objects.get(id=userId)

        if data['password'] != '':
            checkPassword(data['password'],data['password2'])
            user.set_password(data['password'])
        if data['username'] != '':
            if checkUsernameExists(data['username'], userId):
                if len(data['username']) > 30:
                    return Response({"username": "Username cannot exceed 30 characters"},
                                    status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
                user.username = data['username']
            else:

                return Response({"username": "A User with that username already exists"}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
        if data['firstname'] != '':
            if len(data['firstname']) > 30:
                return Response({"firstname": "firstname cannot exceed 30 characters"},
                                status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
            user.firstname = data['firstname']
        if data['lastname'] != '':
            if len(data['lastname']) > 30:
                return Response({"lastname": "lastname cannot exceed 30 characters"},
                                status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
            user.lastname = data['lastname']
        if data['imgURL'] != '':
            if len(data['imgURL']) > 255:
                return Response({"imgURL": "imgURL cannot exceed 255 characters"},
                                status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
            user.imgURL = data['imgURL']
        user.save()
        return Response({"user": user.getJson()}, status=status.HTTP_200_OK, content_type='application/json')

    def post(self, request):
        ''' Delete user '''
        userId = getUserId(request)
        try:
            user = User.objects.get(id=userId, active=True)
        except:
            return Response("User does not exist", status=status.HTTP_400_BAD_REQUEST)
        user.delete()
        retObj = user.getJson()
        retObj['isActive'] = user.active
        try:
            refresh = request.data['refresh']
            RefreshToken(refresh).blacklist()
        except:
            print("Token expired")
        return Response(retObj, status=status.HTTP_200_OK)
