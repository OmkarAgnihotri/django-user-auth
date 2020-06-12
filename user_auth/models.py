import uuid
import datetime
from django.db import models
from django.contrib.auth.models import  AbstractUser
from django.conf import settings
from .managers import CustomUserManager

# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(unique = True)
    is_verified = models.BooleanField(default=False)
    verification_uuid = models.UUIDField(default = uuid.uuid4)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    objects = CustomUserManager()
    
    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.email

class PasswordResets(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user', on_delete=models.CASCADE)
    verification_token = models.UUIDField(default = uuid.uuid4)
    created = models.DateTimeField(auto_now_add = True)

