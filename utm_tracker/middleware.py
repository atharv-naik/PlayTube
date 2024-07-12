import re

from django.db import models
from django.utils.deprecation import MiddlewareMixin

from .models import Traffic, Source, SiteHit


class DetectBotsMiddleware:
    BOT_USER_AGENTS = [
        re.compile(r"bot", re.I),
        re.compile(r"crawl", re.I),
        re.compile(r"spider", re.I),
        re.compile(r"slurp", re.I),
        re.compile(r"python", re.I),
        re.compile(r"curl", re.I),
        re.compile(r"wget", re.I),
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        request.is_bot = any(bot.search(user_agent)
                             for bot in self.BOT_USER_AGENTS)
        return self.get_response(request)


class VisitsTrackerMiddleware(MiddlewareMixin):
    REF_STRING = 'via'
    IGNORE_PATHS = ['/admin', '/static', '/media', '/api']

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

    def process_request(self, request):
        # Ignore bots and specific paths
        if request.is_bot or any(request.path.startswith(prefix) for prefix in self.IGNORE_PATHS):
            return

        # Get request metadata
        ip_address = self.get_client_ip(request)
        http_from = request.META.get('HTTP_FROM')
        user_agent = request.META.get('HTTP_USER_AGENT')
        referer = request.META.get('HTTP_REFERER')

        # Ignore self-refering requests
        if referer and (
            request.build_absolute_uri().startswith(
                referer) or referer.startswith(request.build_absolute_uri())
        ):
            return

        # Determine the source of the traffic
        source_name = request.GET.get(self.REF_STRING, 'direct')
        src, _ = Source.objects.get_or_create(name=source_name)
        traffic_source, _ = Traffic.objects.get_or_create(source=src)

        # Increment visits and update traffic source
        traffic_source.visits = models.F('visits') + 1
        traffic_source.ip_address = ip_address
        traffic_source.http_from = http_from
        traffic_source.user_agent = user_agent
        traffic_source.http_referer = referer
        traffic_source.save()

        # Save site hit
        SiteHit.objects.create(
            ip_address=ip_address,
            http_from=http_from,
            user_agent=user_agent,
            http_referer=referer,
            source=src
        )
