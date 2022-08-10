"""SoFolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from .views import PostAPIVIEW, PostOtherAPIVIEW, PostCommentAPIVIEW


@permission_classes([IsAuthenticated])
class Home(generics.GenericAPIView):

    def get(self, request):
        return Response("Sofolio-django-backend")


PREFIX = 'api/'
urlpatterns = [
    path('', PostAPIVIEW.as_view(), name='post'),
    path('user/<str:username>/', PostOtherAPIVIEW.as_view(),
         name='Get posts of a user'),
    path('<str:postId>/', PostAPIVIEW.as_view(), name='interact with a post'),
    path('comment/<str:postId>/', PostCommentAPIVIEW.as_view(),
         name='interact with a post'),
]
