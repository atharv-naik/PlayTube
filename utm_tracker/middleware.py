from django.db import models
from django.utils.deprecation import MiddlewareMixin

from .models import Traffic, Source, SiteHit


class UTMTrackerMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # ignore all admin, static, media and api requests
        if request.path.startswith('/admin') or request.path.startswith('/static') or request.path.startswith('/media') or request.path.startswith('/api'):
            return
        # ignore self refering requests
        referer = request.META.get('HTTP_REFERER', '')
        if referer and request.build_absolute_uri().startswith(referer):
            return

        if 'via' in request.GET:
            source_name = request.GET['via']
            try:
                src = Source.objects.get(name=source_name)
                traffic_source, _ = Traffic.objects.get_or_create(source=src)
            except Source.DoesNotExist:
                # set traffic_source to direct
                src, _ = Source.objects.get_or_create(name='direct')
                traffic_source, _ = Traffic.objects.get_or_create(source=src)
        else:
            # set traffic_source to direct
            src, _ = Source.objects.get_or_create(name='direct')
            traffic_source, _ = Traffic.objects.get_or_create(source=src)
        
        # increment visits
        traffic_source.visits = models.F('visits') + 1
        traffic_source.save()

        # save site hit
        SiteHit.objects.create(ip_address=request.META.get('REMOTE_ADDR'))

