# from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import LoginAPIVIEW, LogOutAPIVIEW, RegisterAPIVIEW, UpdateProfile
from . import views

# Pattern matching
urlpatterns = [
    # Used to register user
    path('register/', RegisterAPIVIEW.as_view(), name='register'),
    # Used to login user
    path('login/', LoginAPIVIEW.as_view(), name='login'),
    # Used to logout user
    path('logout/', LogOutAPIVIEW.as_view(), name='logout'),
    # Used to update user
    path('update/', UpdateProfile.as_view(), name='update-profile'),
    # Used to delete user
    path('delete/', UpdateProfile.as_view(), name='delete'),
]
