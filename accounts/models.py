from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):

    def create_superuser(self, email, password):

        if password is None:
            raise TypeError('Superusers must have a password.')

        normalized_email = self.normalize_email(email)
        first_name = f"{normalized_email}_first_name"
        last_name = f"{normalized_email}_last_name"
        user = self.create_user(email, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
