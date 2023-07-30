from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import os


# run below command in terminal to start celery worker
# celery -A youtube worker -l info

# ffmpeg -i video.mp4 -vf fps=1/10,scale=120:-1 thumb%d.jpg -hide_banner

@shared_task
def handle_video_post_upload(video_path, video_id, user_email):
    
    '''
    This function will be called when a video is uploaded
    '''
    transcoding = transcode.apply_async(
        args=[video_path, video_id, user_email],
        retry=True,
        retry_policy={
            'max_retries': 3, # max retries before giving up
            'interval_start': 0, # first retry immediately
            'interval_step': 0.2, # wait 0.2s between retries
            'interval_max': 0.2, # but no longer than 0.2s
        }
    )

    # while not transcoding.ready():
    #     pass


    # video_url = f'http://192.168.43.114:8001/watch/?v={video_id}'
    # notify_user.apply_async(
    #     args=[
    #         user_email,
    #         'Video processed successfully', 
    #         f'Your video is ready for viewing at this <a href="{video_url}">link</a>'
    #     ],
    # )



@shared_task
def transcode(video_path, video_id, user_email):
    # output_path
    video_dir = os.path.dirname(video_path)
    video_name = os.path.basename(video_path)

    import subprocess
    # subprocess.run(['ffmpeg', '-i', video_path, '-c:v', 'libx264', '-crf', '23', '-c:a', 'aac', '-b:a', '128k', '-ac', '2', '-strict', '-2', '-y', 'output.mp4'])
    api_endpoint = f'http://0.0.0.0:8001/api/get-video-stream/{video_id}'
    subprocess.run(['./create-hls-vod.sh', video_dir, video_name, api_endpoint])

    os.makedirs(f'{video_dir}/preview_images', exist_ok=True)
    
    subprocess.run([
        'ffmpeg', '-i', video_path, '-vf', 'fps=1/10,scale=120:-1', f'{video_dir}/preview_images/preview%d.jpg', '-hide_banner', '-y'
    ])


    # notify user
    video_url = f'http://192.168.43.114:8001/watch/?v={video_id}'
    send_mail(
        subject='Video processed successfully',
        message='',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
        html_message=f'{video_name.split(".")[0]} is ready for viewing at this <a href="{video_url}">link</a>',
    )


@shared_task
def notify_user(recipient_email, subject, message='', html_message=''):
    '''
    Send email to user
    '''
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[recipient_email],
        fail_silently=False,
        html_message=html_message,
    )

    
