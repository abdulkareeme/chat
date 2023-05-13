from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

"""
add for user
        this from django.conf import settings in your models

and add this in model connections 
        settings.AUTH_USER_MODEL

"""