from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
	oauth_token = models.CharField(max_length=50)
	oauth_token_secret = models.CharField(max_length=50)