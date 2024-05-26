from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .managers import UserManager
from delivery.models import Business


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Manager(models.Model):
    user = models.OneToOneField(User, related_name='manager', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15)
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name='managers', null=True, blank=True
    )

    def __str__(self):
        return f'{self.business}: {self.first_name} {self.last_name} {self.middle_name}'


class Courier(models.Model):
    user = models.OneToOneField(User, related_name='courier', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15)
    telegram_id = models.CharField(max_length=100, null=True, blank=True)
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name='couriers'
    )

    def __str__(self):
        return f'{self.business}: {self.first_name} {self.last_name} {self.middle_name}'


class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15)
    contact = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.middle_name}'
