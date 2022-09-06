from django.db import models
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import AbstractUser, User
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

class Categories(models.Model):
    category_name = models.CharField(max_length=300)
    image = models.ImageField()

    def __str__(self):
        return self.category_name


class Products(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    price =MoneyField(max_digits=14, decimal_places=2, default_currency='KES', default=0)
    images = models.FileField( null=True)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ProductDeals(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    offer =  models.CharField(max_length=300)
    price =MoneyField(max_digits=14, decimal_places=2, default_currency='KES', default=0)
    images = models.FileField( null=True)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

