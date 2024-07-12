import os
import pickle
import logging
import shutil

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from .models import Channel, Video
from .tasks import (delete_s3_directory_task, migrate_to_local_task,
                    migrate_to_s3_task, transcode_task)


# Create a channel for every new user
@receiver(post_save, sender=User)
def create_channel(sender, instance, created, **kwargs):
    if created:
        Channel.objects.create(
            user=instance, name=instance.username, handle=instance.username)


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
        except Exception as e:
            logging.error(
                f"Failed to delete local files in '{meta_data_root_path}': {e}")


@receiver(post_save, sender=Video)
def set_video_duration(sender, instance, created, **kwargs):
    if created:
        instance.duration = instance.get_duration()
        instance.save(update_fields=['duration'])


# Trigger celery process to generate thumbnails and HLS playlist for a video
@receiver(post_save, sender=Video)
def start_video_processing_pipeline(sender, instance, created, **kwargs):
    if instance.video_file and created:
        video_obj = pickle.dumps(instance)
        transcode_task.apply_async(args=[video_obj])


@receiver(pre_save, sender=Video)
def check_video_location_change(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Video.objects.get(pk=instance.pk)
            video_obj = pickle.dumps(instance)
        except Video.DoesNotExist:
            return
        if old_instance.video_location == 'local' and instance.video_location == 's3':
            # handle local -> s3 migration
            migrate_to_s3_task.apply_async(args=[video_obj])
        elif old_instance.video_location == 's3' and instance.video_location == 'local':
            # handle s3 -> local migration
            migrate_to_local_task.apply_async(args=[video_obj])
        else:
            pass
