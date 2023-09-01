from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Channel, Video
from django.contrib.auth.models import User
from .tasks import handle_video_post_upload
import shutil
import os


# Create a channel for every new user
@receiver(post_save, sender=User)
def create_channel(sender, instance, created, **kwargs):
    if created:
        Channel.objects.create(user=instance, name=instance.username, handle=instance.username)

# Delete original video file as well as all media files associated with it when a video is deleted
@receiver(post_delete, sender=Video)
def delete_video(sender, instance, **kwargs):
    if instance.video_file:
        meta_data_root_path = os.path.dirname(instance.video_file.path)
        shutil.rmtree(meta_data_root_path)

@receiver(post_save, sender=Video)
def set_video_duration(sender, instance, created, **kwargs):
    if created:
        instance.duration = instance.get_duration()
        instance.save(update_fields=['duration'])

# Trigger celery process to generate thumbnails and HLS playlist for a video
@receiver(post_save, sender=Video)
def start_celery_preprocess_task(sender, instance, created, **kwargs):
    if instance.video_file:

        handle_video_post_upload.delay(
            instance.video_file.path,
            instance.video_id,
            instance.channel.user.email,
            instance.channel.user.username
        )