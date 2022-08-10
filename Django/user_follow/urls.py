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
from django.urls import path
from .views import FollowAPIVIEW, FollowersAPIVIEW, FollowingAPIVIEW


urlpatterns = [
    # Get (check if follows user), Post make follow if not following, make unfollow if following
    path('<str:username>', FollowAPIVIEW.as_view(), name='follow'),
    path('followers/', FollowersAPIVIEW.as_view(), name='followers'),
    path('following/', FollowingAPIVIEW.as_view(), name='following'),
]
