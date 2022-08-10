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

from .views import PostAPIVIEW, PostOtherAPIVIEW, PostCommentAPIVIEW


urlpatterns = [
    path('', PostAPIVIEW.as_view(), name='post'),
    path('user/<str:username>', PostOtherAPIVIEW.as_view(),
         name='Get posts of a user'),

    path('<str:postId>', PostAPIVIEW.getPostById, name='Get post by postId'),
    
    path('comment/<str:postId>', PostCommentAPIVIEW.as_view(), name='interact with a post'),
]
