from django.db import models
from django.utils.deprecation import MiddlewareMixin

from .models import Via, Source


class UTMTrackerMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # ignore all admin urls
        if request.path.startswith('/admin'):
            return

        if 'via' in request.GET:
            source_name = request.GET['via']
            try:
                src = Source.objects.get(name=source_name)
                source, _ = Via.objects.get_or_create(source=src)
            except Source.DoesNotExist:
                # set source to direct
                src, _ = Source.objects.get_or_create(name='direct')
                source, _ = Via.objects.get_or_create(source=src)
        else:
            # set source to direct
            src, _ = Source.objects.get_or_create(name='direct')
            source, _ = Via.objects.get_or_create(source=src)
        
        # increment visits
        source.visits = models.F('visits') + 1
        source.save()
