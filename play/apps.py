from django.apps import AppConfig
from django.db.models.signals import post_save


class PlayConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'play'

    def ready(self):
        from . import signals
        # post_save.connect(signals.process_video_task, sender='play.Video')
