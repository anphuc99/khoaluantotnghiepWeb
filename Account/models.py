import email
from email.policy import default
from django.db import models

# Create your models here.
class Account(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=35)
    _token = models.CharField(max_length=100, unique=True)
    isUse = models.BooleanField(default = True)