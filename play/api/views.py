from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from play.models import Video, History
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
        'Video Stream': '/api/video/<str:video_id>/<str:file>',
        'Preview Thumbnails': '/api/video/<str:video_id>/preview/<int:number>',
        'Watch History': '/api/history/<str:user>',
        'Update Watch History': '/api/history/<str:user>/<str:video_id>',
    }
    return Response(api_urls)


@api_view(['GET'])
def logo(request):
    file = open('play/static/play/images/PlayTube.png', 'rb')
    response = FileResponse(file)
    return response


@api_view(['GET'])
def getVideoStream(request, video_id, file):
    video = Video.objects.get(video_id=video_id)
    video_path = video.video_file.path
    stream_path = os.path.join(os.path.dirname(video_path), file)
    file = open(stream_path, 'rb')
    response = FileResponse(file)
    return response


@api_view(['GET'])
def getPreviewThumbnails(request, video_id, number):
    video = Video.objects.get(video_id=video_id)
    video_path = video.video_file.path
    stream_path = os.path.join(os.path.dirname(
        video_path), 'preview_images', f'preview{number}.jpg')
    file = open(stream_path, 'rb')
    response = FileResponse(file)
    return response


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getWatchHistory(request, user):
    user = User.objects.get(username=user)
    history = History.objects.filter(channel=user.channel)
    serializer = HistorySerializer(history, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def updateWatchTime(request):
    # check if anonymous user
    if request.user.is_anonymous:
        return Response('User is not logged in')

    video_id = request.POST.get('video_id')
    video = Video.objects.get(video_id=video_id)
    t = int(eval(request.data['timestamp']))

    user = request.user
    # try to update history object for current video and user; create if it doesn't exist
    history, created = History.objects.update_or_create(
        channel=user.channel,
        video=video,
        defaults={'timestamp': t})
    history.save()
    return Response()


@api_view(['POST'])
def updateViews(request):
    video_id = request.POST.get('video_id')
    video = Video.objects.get(video_id=video_id)
    video.views = F('views') + 1
    video.save()
    return Response()
