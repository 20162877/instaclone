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
    # DEFAULT_PIC_URL = "https://placeholde.png"
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name='profile')
    bio = models.CharField(max_length=20, blank=True)
    profile_pic_url = models.ImageField(upload_to='profile_pic/', blank=True)
    is_verified = models.BooleanField(default=True)


# A--->B
# B--->A
# A--->C
# B--->C
# user_a  Who does user_a follow?
# Network.object.filter(from_user=user_a)
# user_a.following.all() --> [B,C]  --> two edges

class NetworkEdge(TimeStamp):
    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="following")
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="follower")

    class Meta:
        # Data won't be insert for same value, if database already has same value
        unique_together = ('from_user', 'to_user',)
