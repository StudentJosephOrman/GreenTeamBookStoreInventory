from django.db import models
from django.core.validators import MinValueValidator


from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Email address is required')
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self.create_user(email, password, **kwargs)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.IntegerField(primary_key=True, default=0)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, blank=True, related_name='user_set', verbose_name='groups')

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    objects = UserManager()

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
    )

    def __str__(self):
        return self.email
    


# SETTER AND GETTER METHODS ARE AUTOMATICALLY CREATED
# DON'T HAVE TO IMPLEMENT, UNLESS ADDITIONAL FUNCTIONALITY IS NEEDED

class Author(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    middle_name = models.CharField(max_length=80)

class Publisher(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=80)
    location = models.CharField(max_length=120)

class Book(models.Model):
    isbn = models.IntegerField(primary_key=True, null=False)
    title = models.CharField(max_length=120)
    author_id = models.ForeignKey(Author, db_column='id', on_delete=models.CASCADE)
    genre = models.CharField(max_length=80)
    publisher_id = models.ForeignKey(Publisher, db_column='id', on_delete=models.CASCADE)
    summary = models.CharField(max_length=120)
    quantity = models.IntegerField()
    cost = models.FloatField(
        validator = [MinValueValidator(0.0)]
    )

class Transaction(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    middle_name = models.CharField(max_length=80)
    book_isbn = models.ForeignKey(Book, db_column='isbn', on_delete=models.CASCADE)
    date = models.DateField()
    cost = models.FloatField(
        validator = [MinValueValidator(0.0)]
    )

class Shipment(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    company = models.CharField(max_length=120)
    expected_date = models.DateField()
    transaction_id = models.ForeignKey(Transaction, db_column='id', on_delete=models.CASCADE)
    cost = models.FloatField(
        validator = [MinValueValidator(0.0)]
    )
    delivered = models.BooleanField()
