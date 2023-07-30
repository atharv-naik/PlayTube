from django.core.exceptions import ValidationError

def validate_video_file(value):
    print('validate_video_file called')
    allowed_formats = ['mp4', 'avi', 'mkv']  # List of allowed video formats
    # set max file size to 2GB
    max_size = 1024 * 1024 * 1024 * 2 # 2GB

    if value:
        file_extension = value.name.split('.')[-1].lower()
        if file_extension not in allowed_formats:
            raise ValidationError("Invalid file format. Only {} formats are allowed.".format(', '.join(allowed_formats)))

        if value.size > max_size:
            raise ValidationError("File size exceeds the maximum limit of 2GB.")
