from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.conf import settings
from play.models import Video
from play.metafile_managers import upload_to_s3, delete_s3_directory, cleanup_local_files

import subprocess
import logging
import os


@shared_task
def transcode_task(info):
    """
    Transcodes video to HLS format and uploads the files to Amazon S3 if indicated.

    Args:
    - info (dict): Information about the video.
    """

    video_path = info['video_path']
    video_id = info['video_id']
    subtitle_path = info['subtitle_path']

    # output_path
    video_dir = os.path.dirname(video_path)

    video = Video.objects.get(video_id=video_id)

    api_endpoint = video.stream_url
    subprocess.run(['./create-hls-vod.sh', video_dir,
                   video_path, api_endpoint, subtitle_path])

    os.makedirs(f'{video_dir}/preview_images', exist_ok=True)

    subprocess.run([
        'ffmpeg', '-i', video_path, '-vf', 'fps=1/10,scale=120:-1', f'{video_dir}/preview_images/preview%d.jpg', '-hide_banner', '-loglevel', 'warning', '-y'
    ])

    if video.video_location == 's3':
        # upload to s3 task
        upload_to_s3_task.apply_async(args=[
            info, video_dir, settings.AWS_STORAGE_BUCKET_NAME, f'videos/{video.channel.channel_id}/{video_id}'
        ])

    # notify user task
    notify_user_task.apply_async(args=[info])


@shared_task
def notify_user_task(info):
    """
    Notifies the user that their video has been processed.
    
    Args:
    - info (dict): Information about the video.
    """

    video_id = info['video_id']
    video = Video.objects.get(video_id=video_id)
    uploader_email = info['uploader_email']
    uploader_name = info['uploader_name']
    video_title = video.title
    domain_name = settings.DOMAIN_NAME

    body = f'Your recent video titled "{video_title}" has been processed and is available to be watched at the below link.'
    html_message = render_to_string('play/email/video_processed.html', {
        'uploader_name': uploader_name,
        'video_title': video_title,
        'message': body,
        'video_url': video.stream_url,
        'domain_name': domain_name,
    })
    plain_message = strip_tags(html_message)
    subject = f'Hey {uploader_name}, your video has been processed. Watch it now!'

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[uploader_email],
        fail_silently=False,
        html_message=html_message
    )


@shared_task
def upload_to_s3_task(info, meta_data_folder_path, bucket_name, s3_key_prefix=''):
    """
    Uploads a folder containing video meta data to Amazon S3 and cleans up the local files.

    Args:
    - info (dict): Information about the video.
    - meta_data_folder_path (str): Path to the folder containing the video meta data.
    - bucket_name (str): Name of the S3 bucket.
    - s3_key_prefix (str): Prefix to prepend to the S3 key.
    """

    result = upload_to_s3(meta_data_folder_path, bucket_name, s3_key_prefix)
    if not result:
        # TODO: Handle failure; possibly retry or notify user
        pass
    logging.info(f"Uploaded S3 files in '{meta_data_folder_path}'.")
    cleanup_local_files(meta_data_folder_path)

    notify_user_task.apply_async(args=[info])


@shared_task
def delete_s3_directory_task(bucket_name, directory):
    """
    Deletes all files in the specified S3 directory.

    Args:
    - bucket_name (str): Name of the S3 bucket.
    - directory (str): Path to the directory to clean up.
    """

    delete_s3_directory(bucket_name, directory)
    logging.info(f"Deleted S3 files in '{directory}'.")
