from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Channel, Video
from django.contrib.auth.models import User
import shutil
import os


# Create a channel for every new user
@receiver(post_save, sender=User)
def create_channel(sender, instance, created, **kwargs):
    if created:
        Channel.objects.create(user=instance, name=instance.username)

# Delete original video file as well as all media files associated with it when a video is deleted
@receiver(post_delete, sender=Video)
def delete_video(sender, instance, **kwargs):
    if instance.video_file:
        meta_data_root_path = os.path.dirname(instance.video_file.path)
        shutil.rmtree(meta_data_root_path)
