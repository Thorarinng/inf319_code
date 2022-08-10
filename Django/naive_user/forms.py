from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms

from user.models import User


# register
# class RegistrationForm(UserCreationForm):
#     email = forms.EmailField(
#         max_length=254, help_text='Required. Add a valid email address.')
#     password1 = forms.PasswordInput(attrs={'class': 'option'})
#     password2 = forms.PasswordInput(attrs={'class': 'option'})
#
#     class Meta:
#         model = User
#         fields = ('email', 'password1', 'password2', 'firstName',
#                   'lastName', 'phoneNumber', 'imgURL')
#         widgets = {
#             'password': forms.PasswordInput(attrs={'class': 'option'}),
#             'email': forms.TextInput(attrs={'class': 'option'}),
#             'password1': forms.TextInput(attrs={'class': 'option'}),
#             'password2': forms.PasswordInput(attrs={'class': 'option'}),
#             'firstName': forms.TextInput(attrs={'class': 'option'}),
#             'lastName': forms.TextInput(attrs={'class': 'option'}),
#             'phoneNumber': forms.TextInput(attrs={'class': 'option'}),
#             'imgURL': forms.TextInput(attrs={'class': 'option'})
#         }
