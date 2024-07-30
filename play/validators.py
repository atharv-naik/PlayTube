import os

from django.core.exceptions import ValidationError


def validate_video_file(value):
    allowed_formats = ['mp4', 'avi', 'mkv']  # List of allowed video formats
    content_types = ['video/mp4', 'video/x-msvideo', 'video/x-matroska']  # List of allowed content types
    # set max file size to 1GB
    max_size_limit = 1024 * 1024 * 1024  # 1GB

    if value.path:
        file_extension = value.name.split('.')[-1].lower()
        content_type = value._file.content_type
        if file_extension not in allowed_formats or content_type not in content_types:
            raise ValidationError(
                f"Invalid file format. Only {', '.join(allowed_formats)} formats are allowed")

        if value._file.size > max_size_limit:
            raise ValidationError(
                "File size exceeds the maximum limit")


def validate_subtitle_file(value):
    allowed_formats = ['srt', 'vtt']
    max_size_limit = 1024 * 1024 * 1  # 1MB

    if value.path:
        file_extension = value.name.split('.')[-1].lower()
        if file_extension not in allowed_formats:
            raise ValidationError(
                f"Invalid file format. Only {', '.join(allowed_formats)} formats are allowed.")

        if value._file.size > max_size_limit:
            raise ValidationError(
                "File size exceeds the maximum limit of 1MB.")


def validate_upload_image_file(value):
    allowed_formats = ['jpg', 'jpeg', 'png']
    max_size_limit = 1024 * 1024 * 2  # 2MB

    if value.path:
        file_extension = value.name.split('.')[-1].lower()
        if file_extension not in allowed_formats:
            raise ValidationError(
                f"Invalid file format. Only {', '.join(allowed_formats)} formats are allowed.")

        if value._file.size > max_size_limit:
            raise ValidationError(
                "File size exceeds the maximum limit of 2MB.")
