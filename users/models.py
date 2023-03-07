from django.db import models
from django.contrib.auth.models import User  # Default user created by Django


# Create your models here.
# class Users(models.Model):
#     name = models.CharField(max_length=30, null=False)
#     password = models.CharField(max_length=20, null=False, default=False)
#     email = models.EmailField(max_length=30, unique=True, null=False)
#     phone_number = models.CharField(max_length=10, unique=True)
#     is_active = models.BooleanField(default=False)
#
#     created_on = models.DateTimeField(auto_now_add=True)
#     last_update = models.DateTimeField(auto_now=True)

class TimeStamp(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(TimeStamp):
    DEFAULT_PIC_URL = "https://placeholde.png"
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    default_pic_url = models.CharField(max_length=50, default=DEFAULT_PIC_URL)
    bio = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=True)
