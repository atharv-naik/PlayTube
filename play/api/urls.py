from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('get-video-stream/<str:video_id>/<str:file>', views.getVideoStream, name='get-video-stream'),
    path('get-preview-thumbnails/<str:video_id>/<int:number>', views.getPreviewThumbnails, name='get-preview-thumbnails'),
    path('update-watch-time/', views.updateWatchTime, name='update-watch-time'),
    path('get-watch-history/<str:user>', views.getWatchHistory, name='get-watch-history'),
    path('update-views/', views.updateViews, name='update-views'),
    path('logo/', views.logo, name='logo'),
    path('get-video-thumbnail/<str:video_id>', views.getVideoThumbnail, name='get-video-thumbnail'),
    path('get-channel-banner/<str:channel_id>', views.getChannelBanner, name='get-channel-banner'),
    
    # V2 API
    path('v2/video/<str:video_id>/<str:file>', views.getVideoStream, name='get-video-stream'),
    path('v2/video/<str:video_id>/preview_images/<str:file>', views.getPreviewThumbnails, name='get-preview-thumbnails'),
]