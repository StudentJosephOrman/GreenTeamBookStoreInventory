from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegister(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

class UserLogin(forms.Form):
    email = forms.CharField(max_length=80, required=True)
    password = forms.CharField(max_length=80, required=True, widget=forms.PasswordInput)

class EditBook(forms.Form):
    isbn = forms.IntegerField(required=True)
    author_ids = forms.CharField(max_length=80, required=True)
    publisher_id = forms.IntegerField()
    summary = forms.CharField(max_length=120, required=True)
    genre = forms.CharField(max_length=80, required=True)
    title = forms.CharField(max_length=80, required=True)
    cost = forms.FloatField(min_value=0.0)