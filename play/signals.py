from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Video
from django.contrib.auth.models import User
import ffmpeg
from youtube.settings import MEDIA_ROOT
import subprocess
import whisper
# from .tasks import process_video_task


# @receiver(post_save, sender=Video)
# def pre_process_video(sender, instance, created, **kwargs):
#     if created:
#         process_video_task.delay(instance.video_file.path, instance.video_id)

# @receiver(post_save, sender=Video)
# def pre_process_video(sender, **kwargs):
#     print('pre-processing video')
#     # do something with the video
#     # ...
#     # get the video file
#     instance = kwargs.get('instance')
#     video_file = instance.video_file
#     video_path = video_file.path
#     output_path = MEDIA_ROOT / f'streams/{instance.video_id}.m3u8'
#     # convert into .m3u8 format
#     # print(output_path, video_path)
#     # inpt = ffmpeg.input(video_path)
#     # inpt.output(filename=output_path, 
#     #                             vf='scale=640:360',
#     #                             **{
#     #                                 'hls_time': 10,
#     #                                 'hls_list_size': 0,
#     #                                 'start_number': 0,
#     #                                 'hls_flags': 'delete_segments',
#     #                                 'preset': 'ultrafast',
#     #                                 'profile:v': 'baseline',
#     #                                 'level': '3.0',
#     #                                 'f': 'hls'
#     #                             }).run()
#     ffmpeg_command = [
#         'ffmpeg',
#         '-i', video_path,
#         '-profile:v', 'baseline',
#         '-level', '3.0',
#         '-s', '640x360',
#         '-start_number', '0',
#         '-hls_time', '10',
#         '-hls_list_size', '0',
#         '-f', 'hls',
#         output_path
#     ]

#     subprocess.call(ffmpeg_command)

# after video is uploaded, create a celery instance for pre-processing the video
# includes converting the video into .m3u8 format using ffmpeg, and if user chose auto generate subtitles, then generate subtitles
# using the subsai library 
# after pre-processing is done, update the video status to 'processed'
# after video is processed, create a celery instance to notify the channel user that the video is done processing


# @receiver(post_save, sender=User)
# def create_channel(sender, **kwargs):
#     print('creating channel')
#     instance = kwargs.get('instance')
#     if kwargs.get('created'):
#         # create a channel for the user
#         from .models import Channel
#         Channel.objects.create(
#             name=instance.username,
#             handle=instance.username,
#             user=instance
#         )