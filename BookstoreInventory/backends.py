from django.contrib.auth.backends import ModelBackend
from .models import User


class UserBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            customer = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        else:
            if customer.check_password(password):
                return customer
        return None