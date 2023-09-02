from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'play'
urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('results/', views.results, name='results'),
    path('upload/', views.videoUpload, name='upload-video'),
    path('watch/', views.watch, name='watch'),
    path('@<str:handle>/', views.channel_via_handle, name='channel-via-handle'),
    path('channel/<str:channel_id>/', views.channel_via_id, name='channel-via-id'),
    path('history/', views.history, name='history'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'play.views.error_404'