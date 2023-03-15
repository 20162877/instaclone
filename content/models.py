from django.db import models

# Create your models here.
from users.models import TimeStamp, UserProfile


class UserPost(TimeStamp):
    caption_text = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=200, null=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='post')


class PostMedia(TimeStamp):
    # ToDO: limit this field to accept files of certain type and size : Validator attr
    media_file = models.FileField(upload_to='post_media/')
    sequence_index = models.PositiveSmallIntegerField(default=8)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='media')

    class Meta:
        unique_together = ('sequence_index', 'post',)
