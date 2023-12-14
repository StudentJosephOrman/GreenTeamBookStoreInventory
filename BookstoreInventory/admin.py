from django.contrib import admin
from .models import User, UserManager, Transaction

# This python script is a built-in DJango script, but allows us to modify what is viewable on their automatic
# admin page.

admin.site.register(User)

