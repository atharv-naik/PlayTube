from __future__ import absolute_import, unicode_literals

import logging
import os
import pickle
import subprocess

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from play.metafile_managers import (amend_manifest, cleanup_local_files,
                                    delete_s3_directory, download_from_s3,
                                    upload_to_s3)


@shared_task
def transcode_task(video_obj):
    """
    Transcodes video to HLS format and uploads the files to Amazon S3 if indicated.

    Args:
    - video_obj (bytes): Pickled video object.
    """

    video = pickle.loads(video_obj)

    video_path = video.video_file.path
    api_endpoint = video.stream_url
    subtitle_path = video.subtitle.path if video.subtitle else ""

    video_dir = os.path.dirname(video_path)
    # create HLS VOD
    subprocess.run([
        './create-hls-vod.sh', video_dir, video_path, api_endpoint, subtitle_path
    ])

    # create preview images
    os.makedirs(f'{video_dir}/preview_images', exist_ok=True)
    subprocess.run([
        'ffmpeg', '-i', video_path, '-vf', 'fps=1/10,scale=120:-1', f'{video_dir}/preview_images/preview%d.jpg', '-hide_banner', '-loglevel', 'warning', '-y'
    ])

    if video.video_location == 's3':
        # upload to s3 task
        upload_to_s3_task.apply_async(args=[video_obj])
    else:
        # notify user task
        notify_user_task.apply_async(args=[video_obj])


@shared_task
def notify_user_task(video_obj):
    """
    Notifies the user that their video has been processed.

    Args:
    - video_obj (bytes): Pickled video object.
    """

    video = pickle.loads(video_obj)

    uploader_email = video.channel.user.email
    uploader_name = video.channel.user.username

    body = f'Your recent video titled "{video.title}" has been processed and is available to be watched at the below link.'
    html_message = render_to_string('play/email/video_processed.html', {
        'uploader_name': uploader_name,
        'video_title': video.title,
        'message': body,
        'video_url': video.stream_url,
        'domain_name': settings.DOMAIN_NAME,
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
def upload_to_s3_task(video_obj):
    """
    Uploads a folder containing video meta data to Amazon S3 and cleans up the local files.

    Args:
    - video_obj (bytes): Pickled video object.
    """

    video = pickle.loads(video_obj)

    video_dir = os.path.dirname(video.video_file.path)
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    s3_key_prefix = f'videos/{video.channel.channel_id}/{video.video_id}'

    try:
        upload_to_s3(
            meta_data_folder_path=video_dir,
            bucket_name=bucket_name,
            s3_key_prefix=s3_key_prefix
        )
    except Exception as e:
        logging.error(f"Failed to upload files to S3. Aborting: {e}")
        # cleanup intermitant s3 files
        delete_s3_directory(
            bucket_name=bucket_name,
            s3_key=s3_key_prefix
        )
    else:
        logging.info(f"Uploaded files to S3")

        cleanup_local_files(video_dir=video_dir)

        # notify user task
        notify_user_task.apply_async(args=[video_obj])


@shared_task
def migrate_to_s3_task(video_obj):
    """
    Migrates the video metafiles from local storage to Amazon S3.

    Args:
    - video_obj (bytes): Pickled video object.
    """

    video = pickle.loads(video_obj)

    video_id = video.video_id
    video_dir = os.path.dirname(video.video_file.path)
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    s3_key_prefix = f'videos/{video.channel.channel_id}/{video_id}'

    try:
        # amend manifest to point to s3 before uploading
        amend_manifest(video_obj)

        upload_to_s3(
            meta_data_folder_path=video_dir,
            bucket_name=bucket_name,
            s3_key_prefix=s3_key_prefix
        )
    except Exception as e:
        logging.error(f"Failed to migrate local files to S3: {e}\nAborting.")
        # cleanup intermitant s3 files
        delete_s3_directory(
            bucket_name=bucket_name,
            s3_key=s3_key_prefix
        )

        # rollback amends to manifest
        amend_manifest(video_obj, revert=True)
    else:
        logging.info(f"Moved local files in '{video_dir}' to S3")

        # update stream_url
        video.stream_url = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/videos/{video.channel.channel_id}/{video_id}'
        video.save(update_fields=['stream_url'])

        # cleanup local files
        cleanup_local_files(video_dir)


@shared_task
def delete_s3_directory_task(bucket_name, s3_key):
    """
    Deletes all files in the specified S3 directory.

    Args:
    - bucket_name (str): Name of the S3 bucket.
    - directory (str): Path to the directory to clean up (s3 key prefix).
    """

    delete_s3_directory(bucket_name, s3_key)


@shared_task
def migrate_to_local_task(video_obj):
    """
    Migrates the video metafiles from Amazon S3 to local storage.

    Args:
    - video_obj (bytes): Pickled video object.
    """

    video = pickle.loads(video_obj)
    s3_key = f'videos/{video.channel.channel_id}/{video.video_id}'
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    video_dir = os.path.dirname(video.video_file.path)

    try:
        download_from_s3(
            bucket_name=bucket_name,
            s3_key=s3_key
        )
    except Exception as e:
        logging.error(
            f"Failed to migrate S3 files to local storage: {e}\nAborting.")
        # cleanup intermetant local files
        cleanup_local_files(video_dir)
    else:
        logging.info(f"Moved S3 files in '{s3_key}' to '{video_dir}'")

        # update stream_url
        http_protocol = 'https' if settings.USE_HTTPS else 'http'
        video.stream_url = f'{http_protocol}://{settings.DOMAIN_NAME}/api/v2/video/{video.video_id}'
        video.save(update_fields=['stream_url'])

        # cleanup s3 files
        delete_s3_directory(
            bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
            s3_key=s3_key
        )

        # amend manifest to point back to local storage
        amend_manifest(video_obj, revert=True)
