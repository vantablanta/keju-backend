from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Users(AbstractUser):
    name = models.CharField(max_length=300)
    email = models.CharField(max_length=300, unique=True)
    password = models.CharField(max_length=300)
    username = models.CharField(max_length=300, blank=True)

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self):
        return self.email