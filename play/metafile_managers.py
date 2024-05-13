import os
import shutil
import logging

import boto3


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

    Returns:
    - bool: True if upload is successful, False otherwise.
    """

    # Ensure the folder exists
    if not os.path.isdir(meta_data_folder_path):
        logging.error(f"Folder '{meta_data_folder_path}' does not exist.")
        return False

    # Initialize S3 client
    s3 = boto3.client('s3')

    # Iterate through files in the folder and upload them to S3
    for root, dirs, files in os.walk(meta_data_folder_path):
        for file in files:
            local_file_path = os.path.join(root, file)
            s3_key = os.path.join(s3_key_prefix, os.path.relpath(local_file_path, meta_data_folder_path))
            
            # Upload the file to S3
            try:
                s3.upload_file(local_file_path, bucket_name, s3_key, ExtraArgs={'ACL': 'public-read'})
                logging.info(f"Uploaded '{local_file_path}' to '{bucket_name}/{s3_key}'.")
            except Exception as e:
                logging.error(f"Failed to upload '{local_file_path}' to '{bucket_name}/{s3_key}': {e}")
                return False

    return True


def delete_s3_directory(bucket_name, directory):
    """
    Delete a directory (and all its contents) on Amazon S3.

    Args:
    - bucket_name (str): Name of the S3 bucket.
    - directory (str): Path of the directory to be deleted (e.g., 'path/to/directory/').
    """

    s3 = boto3.client('s3')

    # list objects in the directory
    objects_to_delete = []
    paginator = s3.get_paginator('list_objects_v2')
    for result in paginator.paginate(Bucket=bucket_name, Prefix=directory):
        if 'Contents' in result:
            for obj in result['Contents']:
                objects_to_delete.append({'Key': obj['Key']})

    # delete objects
    if len(objects_to_delete) > 0:
        s3.delete_objects(Bucket=bucket_name, Delete={'Objects': objects_to_delete})

    logging.info(f"Deleted {len(objects_to_delete)} objects from directory '{directory}' in bucket '{bucket_name}'.")
