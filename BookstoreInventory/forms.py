from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegister(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

class UserLogin(forms.Form):
    email = forms.CharField(max_length=80, required=True)
    username = forms.CharField(max_length=80, required=True)
    password = forms.CharField(max_length=80, required=True, widget=forms.PasswordInput)