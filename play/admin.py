from django.contrib import admin

# Register your models here.

from .models import Channel, Comment, Dislike, Like, Subscription, Video, View

admin.site.register(Channel)
admin.site.register(Comment)
admin.site.register(Dislike)
admin.site.register(Like)
admin.site.register(Subscription)
admin.site.register(Video)
admin.site.register(View)
