import logging
import os
import pickle
import shutil

import boto3
from django.conf import settings


def cleanup_local_files(video_dir):
    """
    Deletes all files in the specified directory.

    Args:
    - video_dir (str): Path to the directory to clean up.
    """

    try:
        shutil.rmtree(video_dir)
        logging.info(f"Deleted local files in '{video_dir}'.")
    except Exception as e:
        logging.error(f"Failed to delete local files in '{video_dir}': {e}")


def upload_to_s3(meta_data_folder_path, bucket_name, s3_key_prefix=''):
    """
    Uploads a folder containing video meta data to Amazon S3.

    Args:
    - meta_data_folder_path (str): Path to the folder containing video meta data.
    - bucket_name (str): Name of the S3 bucket to upload to.
    - s3_key_prefix (str): Optional prefix to prepend to S3 keys.
    """

    # Initialize S3 client
    s3 = boto3.client('s3')

    # Iterate through files in the folder and upload them to S3
    for root, dirs, files in os.walk(meta_data_folder_path):
        for file in files:
            local_file_path = os.path.join(root, file)
            s3_key = os.path.join(s3_key_prefix, os.path.relpath(
                local_file_path, meta_data_folder_path))

            # Upload the file to S3
            s3.upload_file(local_file_path, bucket_name, s3_key,
                           ExtraArgs={'ACL': 'public-read'})
            logging.info(
                f"Uploaded '{local_file_path}' to '{bucket_name}/{s3_key}'.")


def delete_s3_directory(bucket_name, s3_key):
    """
    Delete a directory (and all its contents) on Amazon S3.

    Args:
    - bucket_name (str): Name of the S3 bucket.
    - s3_key (str): Path to the directory to delete.
    """

    s3 = boto3.client('s3')

    # list objects in the directory
    objects_to_delete = []
    paginator = s3.get_paginator('list_objects_v2')
    for result in paginator.paginate(Bucket=bucket_name, Prefix=s3_key):
        if 'Contents' in result:
            for obj in result['Contents']:
                objects_to_delete.append({'Key': obj['Key']})

    # delete objects
    if len(objects_to_delete) > 0:
        s3.delete_objects(Bucket=bucket_name, Delete={
                          'Objects': objects_to_delete})

    logging.info(
        f"Deleted {len(objects_to_delete)} objects from directory '{s3_key}' in bucket '{bucket_name}'.")


def download_from_s3(bucket_name, s3_key):
    """
    Downloads a directory from Amazon S3.

    Args:
    - bucket_name (str): Name of the S3 bucket.
    - s3_key (str): Path to the directory to download in the S3 bucket.
    """

    s3 = boto3.client('s3')

    # List objects in the directory
    paginator = s3.get_paginator('list_objects_v2')
    for result in paginator.paginate(Bucket=bucket_name, Prefix=s3_key):
        if 'Contents' in result:
            for obj in result['Contents']:
                s3_key = obj['Key']

                local_file_path = os.path.abspath(f'media/{s3_key}')

                # create the local directory structure
                os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

                logging.info(
                    f"Downloading '{bucket_name}/{s3_key}' to '{local_file_path}'...")

                # Download the file
                s3.download_file(bucket_name, s3_key, local_file_path)


# File amendments helpers

def amend_manifest(video_obj, revert=False):
    """
    Amends the manifest file to point to the S3 bucket.

    Args:
    - video_obj (bytes): Pickled Video object.
    - revert (bool): If True, reverts and point back to local storage.
    """

    video = pickle.loads(video_obj)
    file_path = os.path.join(os.path.dirname(
        video.video_file.path), 'playlist.m3u8')

    if not os.path.exists(file_path):
        logging.error(f"Manifest file not found at '{file_path}'")
        return

    local_url_prefix = [
        rf"{'https' if settings.USE_HTTPS else 'http'}://{settings.DOMAIN_NAME}/api/v2/video",
        rf"{'https' if settings.USE_HTTPS else 'http'}://{settings.DOMAIN_NAME}/api/get-video-stream"
    ]

    s3_url_prefix = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/videos/{video.channel.channel_id}'

    with open(file_path, 'r') as f:
        lines = f.readlines()

    with open(file_path, 'w') as f:
        if revert:
            for line in lines:
                if s3_url_prefix in line:
                    line = line.replace(s3_url_prefix, local_url_prefix[0])
                f.write(line)
        else:
            for line in lines:
                for prefix in local_url_prefix:
                    if prefix in line:
                        line = line.replace(prefix, s3_url_prefix)
                f.write(line)

    logging.info(f"Amended m3u8 file at '{file_path}'")
