from django.contrib import admin
from .models import Source, Traffic, SiteHit
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

class TrafficAdmin(admin.ModelAdmin):

    list_display = ("source", "visits", "last_visit")
    search_fields = ("source__name",)
    list_filter = ("source",)
    readonly_fields = ("visits", "last_visit")

    change_list_template = "admin/change_list.html"
    def changelist_view(self, request, extra_context=None):
        hits_data = (
            SiteHit.objects.annotate(date=models.functions.TruncDay("timestamp")).values("date").annotate(hits=models.Count("id")
            ).order_by("-date")
        )
        hits_data = json.dumps(list(hits_data), cls=DjangoJSONEncoder)

        traffic_data = (
            Traffic.objects.values("source", "visits")
        )
        traffic_data = json.dumps(list(traffic_data), cls=DjangoJSONEncoder)

        total_hits = SiteHit.objects.count()
        extra_context = extra_context or {
            "hits_data": hits_data, 
            "traffic_data": traffic_data,
            "total_hits": total_hits,
            "show_stats": True
        }
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Traffic, TrafficAdmin)

admin.site.register(Source)

