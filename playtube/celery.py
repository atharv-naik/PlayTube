import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'playtube.settings')

app = Celery('playtube')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.Task.track_started = True

# # enable task routing
# app.conf.task_routes = {
#     'play.tasks.transcode': {'queue': 'video-processing'},
#     'play.tasks.notify_user': {'queue': 'email'},
# }

app.autodiscover_tasks()
