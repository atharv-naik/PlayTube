from rest_framework.decorators import api_view
from rest_framework.response import Response
from play.models import Video
from django.http import FileResponse
import os

# Create your views here.

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/video-list/',
        'Detail View': '/video-detail/<str:pk>/',
        'Create': '/video-create/',
        'Update': '/video-update/<str:pk>/',
        'Delete': '/video-delete/<str:pk>/',
    }
    return Response(api_urls)

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
    stream_path = os.path.join(os.path.dirname(video_path), 'preview_images', f'preview{number}.jpg')
    file = open(stream_path, 'rb')
    response = FileResponse(file)
    return response

