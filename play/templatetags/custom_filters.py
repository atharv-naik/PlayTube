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

def leadingZeroFormatter(value):
    if value < 10:
        return f'0{value}'
    return value

@register.filter
def get_duration_stamp(duration):
    duration = int(duration)
    hours = duration // 3600
    minutes = (duration - (hours * 3600)) // 60
    seconds = duration - (hours * 3600) - (minutes * 60)
    if hours == 0:
        return f'{minutes}:{leadingZeroFormatter(seconds)}'
    return f'{hours}:{leadingZeroFormatter(minutes)}:{leadingZeroFormatter(seconds)}'

@register.filter
def truncatetimesince(value):
    return value.split(',')[0]
