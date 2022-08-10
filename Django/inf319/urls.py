"""inf319 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from telnetlib import STATUS
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView
from .schema import schema

PREFIX = 'api/'


def home(request):
    return JsonResponse({"ba": 0}, status=status.HTTP_200_OK)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Here we use the same model because it is the default auth to the service
    path(f'{PREFIX}naive/user/', include('naive_user.urls')),
    path(f'{PREFIX}user/', include('user.urls')),

    # Naive paths
    path(f'{PREFIX}naive/post/', include('naive_post.urls')),
    path(f'{PREFIX}naive/like/', include('naive_post.urls')),
    path(f'{PREFIX}naive/follow/', include('naive_follow.urls')),

    # REST paths
    path(f'{PREFIX}post/', include('user_post.urls')),
    path(f'{PREFIX}like/', include('post_like.urls')),
    path(f'{PREFIX}follow/', include('user_follow.urls')),

    # GraphQL
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]
