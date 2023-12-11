from django import template
from moviepy.editor import VideoFileClip

register = template.Library()

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

@register.filter
def format_views(views):
    if views < 1000:
        return views
    elif views < 1000000:
        return f'{views // 1000}K'
    elif views < 1000000000:
        return f'{views // 1000000}M'
    
    return f'{views // 1000000000}B'
