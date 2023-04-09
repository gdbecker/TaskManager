from django.db import models
from django.contrib import auth

# Create your models here.
# accounts

class User(auth.models.User, auth.models.PermissionsMixin):
    def __str__(self):
        return self.username
