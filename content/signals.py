from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import PostMedia, UserPost


# TODO Call celery method to process media

@receiver(post_save, sender=PostMedia)
def process_media(sender, instance, **kwargs):
    print("inside post process media signal")
