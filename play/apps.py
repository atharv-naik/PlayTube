from django.apps import AppConfig


class PlayConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'play'

    def ready(self):
        import play.signals
