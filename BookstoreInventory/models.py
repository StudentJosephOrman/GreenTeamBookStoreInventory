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
    

# ENUM Class, not a DB Model
class USER_TYPE:
    DEFAULT:int = 0
    EMPLOYEE:int = 1
    ADMIN:int = 2
    MANAGER:int = 3

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=80)
    user_type = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, blank=True, related_name='user_groups', verbose_name='groups')

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    objects = UserManager()

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_permissions',
        verbose_name='user permissions',
        blank=True,
    )

    def __str__(self):
        return self.email
    

# Note:
# AN AUTO_INCREMENT ID FIELD IS AUTOMATICALLY CREATED
# SETTER AND GETTER METHODS ARE AUTOMATICALLY CREATED
# DON'T HAVE TO IMPLEMENT, UNLESS ADDITIONAL FUNCTIONALITY IS NEEDED


class Author(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    middle_name = models.CharField(max_length=80)

class Publisher(models.Model):
    name = models.CharField(max_length=80, unique=True)
    location = models.CharField(max_length=120)

class Book(models.Model):
    isbn = models.IntegerField(primary_key=True, null=False)
    title = models.CharField(max_length=120)
    authors = models.ManyToManyField(Author, db_column='author_ids')
    genre = models.CharField(max_length=80)
    publisher = models.ForeignKey(Publisher, db_column='publisher_id', on_delete=models.CASCADE)
    summary = models.CharField(max_length=120)
    quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    cost = models.FloatField(
        default=0.0,
        validators = [MinValueValidator(0.0)]
    )

class Transaction(models.Model):
    book_isbn = models.IntegerField(default=0)
    date = models.DateField()
    cost = models.FloatField(
        default=0.0,
        validators = [MinValueValidator(0.0)]
    )
    quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

class Shipment(models.Model):
    company = models.CharField(max_length=120)
    expected_date = models.DateField()
    transaction = models.ForeignKey(Transaction, db_column='transaction_id', on_delete=models.CASCADE)
    cost = models.FloatField(
        default=0.0,
        validators = [MinValueValidator(0.0)]
    )
    delivered = models.BooleanField()
