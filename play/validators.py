import os

from django.core.exceptions import ValidationError


def validate_video_file(value):
    allowed_formats = ['mp4', 'avi', 'mkv']  # List of allowed video formats
    # set max file size to 30MB
    max_size = 1024 * 1024 * 30  # 30MB

    if os.path.exists(value.path):
        file_extension = value.name.split('.')[-1].lower()
        if file_extension not in allowed_formats:
            raise ValidationError(
                f"Invalid file format. Only {', '.join(allowed_formats)} formats are allowed.")

        if value.size > max_size:
            raise ValidationError(
                "File size exceeds the maximum limit of 30MB.")


def validate_subtitle_file(value):
    allowed_formats = ['srt', 'vtt']
    max_size = 1024 * 1024 * 1  # 1MB

    if os.path.exists(value.path):
        file_extension = value.name.split('.')[-1].lower()
        if file_extension not in allowed_formats:
            raise ValidationError(
                f"Invalid file format. Only {', '.join(allowed_formats)} formats are allowed.")

        if value.size > max_size:
            raise ValidationError(
                "File size exceeds the maximum limit of 1MB.")


def validate_upload_image_file(value):
    allowed_formats = ['jpg', 'jpeg', 'png']
    max_size = 1024 * 1024 * 2  # 2MB

    if os.path.exists(value.path):
        file_extension = value.name.split('.')[-1].lower()
        if file_extension not in allowed_formats:
            raise ValidationError(
                f"Invalid file format. Only {', '.join(allowed_formats)} formats are allowed.")

        if value.size > max_size:
            raise ValidationError(
                "File size exceeds the maximum limit of 2MB.")
