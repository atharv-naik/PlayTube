from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Channel, Video
from django.contrib.auth.models import User
from .tasks import transcode_task, delete_s3_directory_task
from play.metafile_managers import delete_s3_directory
from django.conf import settings
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
        if instance.video_location == 's3':
            # Network I/O; run in background
            delete_s3_directory_task.apply_async(args=[
                settings.AWS_STORAGE_BUCKET_NAME, f'videos/{instance.channel.channel_id}/{instance.video_id}'
            ])
        
        meta_data_root_path = os.path.dirname(instance.video_file.path)
        try:
            shutil.rmtree(meta_data_root_path)
        except FileNotFoundError:
            pass

@receiver(post_save, sender=Video)
def set_video_duration(sender, instance, created, **kwargs):
    if created:
        instance.duration = instance.get_duration()
        instance.save(update_fields=['duration'])

# Trigger celery process to generate thumbnails and HLS playlist for a video
@receiver(post_save, sender=Video)
def start_video_processing_pipeline(sender, instance, created, **kwargs):
    if instance.video_file and created:

        info = {
            'video_path': instance.video_file.path,
            'video_id': instance.video_id,
            'subtitle_path': instance.subtitle.path if instance.subtitle else "",
            'uploader_email': instance.channel.user.email,
            'uploader_name': instance.channel.user.username
        }

        transcode_task.apply_async(args=[info])
