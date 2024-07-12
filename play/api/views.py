from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from play.models import Video, History, Channel
from django.http import FileResponse
from .serializers import HistorySerializer
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.db.models import F
import os

# Create your views here.


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Get Video Stream': '/get-video-stream/<str:video_id>/<str:file>',
        'Get Preview Thumbnails': '/get-preview-thumbnails/<str:video_id>/<int:number>',
        'Update Watch Time': '/update-watch-time/',
        'Get Watch History': '/get-watch-history/<str:user>',
        'Update Views': '/update-views/',
        'Logo': '/logo/',
        'Get Video Thumbnail': '/get-video-thumbnail/<str:video_id>',
        'Get Channel Banner': '/get-channel-banner/<str:channel_id>',

        # V2 API
        'Get Video Stream V2': '/v2/video/<str:video_id>/<str:file>',
        'Get Preview Thumbnails V2': '/v2/video/<str:video_id>/preview_images/<str:file>',
    }
    return Response(api_urls)


@api_view(['GET'])
def logo(request):
    file = open('static/play/images/v2/PlayTube-icon-full.png', 'rb')
    return FileResponse(file, status=200)


@api_view(['GET'])
def getVideoStream(request, video_id, file):
    video = get_object_or_404(Video, video_id=video_id)
    # visibility checks
    if video.visibility == 'private':
        if request.user.is_anonymous:
            return Response(status=401)
        if request.user.channel != video.channel:
            return Response(status=403)

    video_path = video.video_file.path
    stream_path = os.path.join(os.path.dirname(video_path), file)
    try:
        file = open(stream_path, 'rb')
    except FileNotFoundError:
        return Response(status=404)
    return FileResponse(file, status=200)


@api_view(['GET'])
def getVideoThumbnail(request, video_id):
    video = get_object_or_404(Video, video_id=video_id)
    try:
        file = open(video.thumbnail.path, 'rb')
    except (FileNotFoundError, ValueError):
        file = open('static/play/images/v2/PlayTube-icon-full.png', 'rb')
    return FileResponse(file, status=200)


@api_view(['GET'])
def getPreviewThumbnails(request, video_id, file):
    video = get_object_or_404(Video, video_id=video_id)
    video_path = video.video_file.path
    stream_path = os.path.join(os.path.dirname(
        video_path), 'preview_images', file)
    try:
        file = open(stream_path, 'rb')
    except FileNotFoundError:
        return Response(status=404)
    return FileResponse(file, status=200)


@api_view(['GET'])
def getChannelBanner(request, channel_id):
    channel = get_object_or_404(Channel, channel_id=channel_id)
    try:
        file = open(channel.banner.path, 'rb')
    except (FileNotFoundError, ValueError):
        file = open('static/play/images/v2/PlayTube-icon-full.png', 'rb')
    return FileResponse(file, status=200)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getWatchHistory(request, user):
    user = get_object_or_404(User, username=user)
    history = History.objects.filter(channel=user.channel)
    serializer = HistorySerializer(history, many=True)
    return Response(serializer.data, status=200)


@api_view(['POST'])
def updateWatchTime(request):
    # check if anonymous user
    if not request.user.is_authenticated:
        return Response(status=401)

    video_id = request.POST.get('video_id')
    video = get_object_or_404(Video, video_id=video_id)
    t = int(eval(request.data['timestamp']))

    user = request.user
    # try to update history object for current video and user; create if it doesn't exist
    history, _ = History.objects.update_or_create(
        channel=user.channel,
        video=video,
        defaults={'timestamp': t}
        )
    history.save()
    return Response(status=200)


@api_view(['POST'])
def updateViews(request):
    video_id = request.POST.get('video_id')
    video = get_object_or_404(Video, video_id=video_id)
    video.views = F('views') + 1
    video.save()
    return Response(status=200)
