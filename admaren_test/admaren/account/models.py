from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager

from django.db import models

class User(AbstractUser):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True,)
    REQUIRED_FIELDS = []