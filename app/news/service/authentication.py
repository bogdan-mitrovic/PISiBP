from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django import forms
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    is_superuser = forms.BooleanField(required=False)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'is_superuser')



