from django import template
from moviepy.editor import VideoFileClip

register = template.Library()

@register.filter
def calculate_duration(video):
    try:
        video_clip = VideoFileClip(video.video_file.path)
        return video_clip.duration
    except:
        return 0
