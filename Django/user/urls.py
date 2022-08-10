# from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import LoginAPIVIEW, LogOutAPIVIEW, RegisterAPIVIEW, UpdateProfile
from . import views
#from . import views

# Pattern matching
urlpatterns = [
    path('register/', RegisterAPIVIEW.as_view(), name='register'),
    path('login/', LoginAPIVIEW.as_view(), name='login'),
    path('logout/', LogOutAPIVIEW.as_view(), name='logout'),
    path('update/', UpdateProfile.as_view(), name='update'),
    path('delete/', UpdateProfile.as_view(), name='update'),
]
