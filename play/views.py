from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Video, Channel
from .forms import SignInForm, VideoUploadForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .tasks import handle_video_post_upload
import os


# Create your views here.

# movies_data = open("../../youtube-video-player-clone/movie_data.json", "r").read()
# movies_data_object = json.loads(movies_data)


def loginPage(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('play:home')
        else:
            return redirect('play:login')

    
    form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'play/login_register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('play:home')

def home(request):
    movies = Video.objects.all()
    movies = {'movies': movies}
    return render(request, 'play/landing.html', movies)

def results(request):
    query = request.GET.get('search_query')
    if query is None:
        return redirect('play:home')
    
    movies = Video.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(genre__icontains=query) |
        Q(series_name__icontains=query) |
        Q(channel__name__icontains=query) |
        Q(channel__handle__icontains=query) |
        Q(channel__user__username__icontains=query) |
        Q(release_year__icontains=query)
    )
    if movies.count() == 0:
        # show no results found page
        info = {'info': 'No results found'}
        return render(request, 'play/404.html', info, status=404)
    movies = {'movies': movies, 'search_query': query}
    return render(request, 'play/results.html', movies)

@login_required
def videoUpload(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.channel = request.user.channel
            video.save()
            handle_video_post_upload.delay(video.video_file.path, video.video_id, request.user.email, request.user.first_name)
            return redirect('play:home')
    form = VideoUploadForm()
    return render(request, 'play/upload.html', {'form': form})

def watch(request):
    video_id = request.GET.get('v')
    channel_id = request.GET.get('ab_channel')
    t = request.GET.get('t')
    t = 0 if t is None else t
    if video_id is None and channel_id is None:
        info = {'info': 'This video isn\'t available anymore'}
        return render(request, 'play/404.html', info, status=404)
    try:
        video = Video.objects.get(video_id=video_id)
        channel_id = video.channel.channel_id if channel_id is None else channel_id
        channel = Channel.objects.get(channel_id=channel_id) if channel_id is not None else None
        
        # initialize history object
        try:
            user = request.user
            from .models import History
            # create history object if it doesn't exist
            try:
                history = History.objects.get(user=user, video=video)
                t = history.timestamp if request.GET.get('t') is None else t
            except History.DoesNotExist:
                history = History.objects.create(user=user, video=video, timestamp=t)
                history.save()
        except:
            pass

        stream_path = os.path.join(os.path.dirname(video.video_file.path), 'playlist.m3u8')
        return render(request, 'play/watch.html', {'video_id': video_id, 'channel_id': channel_id, 't': t, 'movie': video, 'channel': channel, 'stream_path': stream_path})



    except Channel.DoesNotExist:
        info = {'info': 'This video isn\'t available anymore'}
        return render(request, 'play/404.html', info, status=404)
    except Video.DoesNotExist:
        info = {'info': 'This video isn\'t available anymore'}
        return render(request, 'play/404.html', info, status=404)
    # return render(request, 'play/watch.html', {'video_id': video_id, 'channel_id': channel_id, 't': t, 'movie': video})


def channel_via_handle(request, handle):
    # search the channel handle in the database, else return 404
    try:
        channel = Channel.objects.get(handle=handle)
        channel_name = channel.name
        user = channel.user.username
    except Channel.DoesNotExist:
        info = {'info': 'Channel does not exist'}
        return render(request, 'play/404.html', info, status=404)
    return HttpResponse(f"Hello, world. You're watching {user}'s channel {channel_name}")
    

def channel_via_id(request, channel_id):
    # search the channel id in the database, else return 404
    try:
        channel = Channel.objects.get(channel_id=channel_id)
        channel_name = channel.name
        user = channel.user.username
    except Channel.DoesNotExist:
        info = {'info': 'Channel does not exist'}
        return render(request, 'play/404.html', info, status=404)
    return HttpResponse(f"Hello, world. You're watching {user}'s channel {channel_name}")

def history(request):
    # get user's watch history
    try:
        user = request.user
        from .models import History
        history = History.objects.filter(user=user)
        history = history.order_by('-last_viewed')
        # history = history.values('video__video_id', 'video__title', 'video__description', 'video__thumbnail', 'timestamp')
        return render(request, 'play/history.html', {'history': history})
    except:
        return redirect('play:login')


# custom error pages
# handle custom 404 error
def error_404(request, exception):
    return render(request, 'play/404.html', {'info': 'The requested url was not found on the server'}, status=404)