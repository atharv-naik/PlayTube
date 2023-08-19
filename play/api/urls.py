from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('get-video-stream/<str:video_id>/<str:file>', views.getVideoStream, name='get-video-stream'),
    path('get-preview-thumbnails/<str:video_id>/<int:number>', views.getPreviewThumbnails, name='get-preview-thumbnails'),
    path('update-watch-history/', views.updateHistory, name='update-history'),
    path('get-watch-history/<str:user>', views.getWatchHistory, name='get-watch-history'),
]