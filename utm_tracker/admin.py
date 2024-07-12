from django.contrib import admin
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
import json

from .models import Source, Traffic, SiteHit


class TrafficAdmin(admin.ModelAdmin):
    list_display = ("source", "visits", "last_visit", "ip_address", "http_from", "user_agent", "http_referer")
    search_fields = ("source__name",)
    list_filter = ("source",)
    readonly_fields = ("visits", "last_visit", "ip_address", "http_from", "user_agent", "http_referer")
    change_list_template = "admin/change_list.html"

    def changelist_view(self, request, extra_context={}):
        hits_data = (
            SiteHit.objects
            .annotate(date=models.functions.TruncDay("timestamp"))
            .values("date")
            .annotate(hits=models.Count("id"))
            .order_by("-date")
        )
        traffic_data = Traffic.objects.values("source", "visits")

        hits_data_json = json.dumps(list(hits_data), cls=DjangoJSONEncoder)
        traffic_data_json = json.dumps(list(traffic_data), cls=DjangoJSONEncoder)
        total_hits = SiteHit.objects.count()

        extra_context.update({
            "hits_data": hits_data_json,
            "traffic_data": traffic_data_json,
            "total_hits": total_hits,
            "show_stats": True,
        })

        return super().changelist_view(request, extra_context=extra_context)


class SiteHitAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "http_from", "timestamp", "source", "user_agent", "http_referer")
    search_fields = ("ip_address", "http_from", "user_agent", "source__name", "http_referer")
    list_filter = ("http_from", "timestamp", "source")
    readonly_fields = ("ip_address", "http_from", "timestamp", "user_agent", "http_referer", "source")


admin.site.register(Source)
admin.site.register(Traffic, TrafficAdmin)
admin.site.register(SiteHit, SiteHitAdmin)
