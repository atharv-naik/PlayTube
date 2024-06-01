from django.contrib import admin

from .models import (Channel, Comment, Dislike, History, Like, Subscription,
                     Video)


def migrate_to_s3_action(modeladmin, request, queryset):
    for video in queryset:
        video.video_location = 's3'
        video.save(update_fields=['video_location'])
    modeladmin.message_user(
        request, "Selected videos are being migrated to S3. This may take some time.", level="WARNING")


migrate_to_s3_action.short_description = "Begin S3 migration"


class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'channel', 'visibility', 'video_location',
                    'genre', 'language', 'release_year', 'views', 'created_at')
    list_filter = ('visibility', 'genre', 'language', 'release_year')
    search_fields = ('title', 'description', 'genre', 'channel__name')
    date_hierarchy = 'created_at'
    ordering = ('-views',)
    readonly_fields = ('video_id', 'created_at', 'updated_at', 'video_file',
                       'views', 'duration', 'stream_url', 'subtitles_available')

    actions = [migrate_to_s3_action]


admin.site.register(Channel)
admin.site.register(Comment)
admin.site.register(Dislike)
admin.site.register(Like)
admin.site.register(Subscription)
admin.site.register(Video, VideoAdmin)
admin.site.register(History)
