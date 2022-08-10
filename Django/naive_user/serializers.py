from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from naive_user.models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=6)
    password = serializers.CharField(max_length=255, min_length=0)
    tokens = serializers.CharField(max_length=68, min_length=6, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = User.objects.get(email=email)

        # DEFAULT DATABASE IS user model and not naive_user
        # user = authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials')

        return {
            "id": user.id,
            'email': user.email,
            'password': password,
            'password2': password,
            'username': user.username,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'imgURL': user.imgURL,
            'date': user.date,
            'tokens': user.tokens(),
        }


class LogOutSerializer(serializers.Serializer):
    pass


class RegisterSerializer(serializers.ModelSerializer):
    tokens = serializers.CharField(max_length=68, min_length=6, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'firstname', 'lastname',
                  'username', 'imgURL', 'tokens']  # Fields that are returned from validate e.g
        extra_kwargs = {
            'password': {'error_messages': {'miss-match': "Passwords do not match"}},
        }

    def create_user(self, data):
        user = User.objects.create_user(data)
        tokens = user.tokens()
        return {"tokens": tokens, "user": user}

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')
        firstname = attrs.get('firstname', '')
        lastname = attrs.get('lastname', '')
        username = attrs.get('username', '')
        imgURL = attrs.get('imgURL', '')

        # Custom ValidationError exception for the password field
        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match'})

        data = self.create_user({"email": email, "password": password, "password2": password2,
                                 "firstname": firstname, "lastname": lastname, "username": username, "imgURL": imgURL})

        return {
            'id': data['user'].id,
            'email': data['user'].email,
            'password': data['user'].password,
            'password2': data['user'].password2,
            'firstname': data['user'].firstname,
            'lastname': data['user'].lastname,
            'username': data['user'].username,
            'imgURL': data['user'].imgURL,
            "tokens": data['tokens'],
        }


class UpdateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'firstname', 'lastname',
                  'username', 'imgURL']  # Fields that are returned from validate e.g

    def update_user(self):
        User.objects.update(self.validated_data)

    def validate(self, attrs):
        email = attrs.get('email', '')
        firstname = attrs.get('firstname', '')
        lastname = attrs.get('lastname', '')
        username = attrs.get('username', '')
        imgURL = attrs.get('imgURL', '')

        return {
            'email': email,
            'firstname': firstname,
            'lastname': lastname,
            'username': username,
            'imgURL': imgURL,
        }
