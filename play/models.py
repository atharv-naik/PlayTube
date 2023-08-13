from django.db import models
from django.contrib.auth.models import User
from shortuuid.django_fields import ShortUUIDField
from django.utils import timezone
from .validators import validate_video_file
import moviepy.editor as mp
import shortuuid
import os

# Create your models here.


class Channel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    channel_id = ShortUUIDField(
        length=22, default=shortuuid.uuid, primary_key=True, editable=False, unique=True)
    handle = models.CharField(max_length=100, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='profile_pictures', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} subscribed to {self.channel.name}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey('Video', on_delete=models.CASCADE)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment[:20]


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey('Video', on_delete=models.CASCADE)
    like = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} likes {self.video.title}'


class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey('Video', on_delete=models.CASCADE)
    dislike = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} dislikes {self.video.title}'


class View(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey('Video', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} viewed {self.video.title}'


def getFileUploadPath(instance, filename):
    return os.path.join('videos', f"{instance.channel.channel_id}", f"{instance.video_id}", f"{instance.title}.{filename.split('.')[-1]}")


class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    video_id = ShortUUIDField(
        length=11, default=shortuuid.uuid, primary_key=True, editable=False, unique=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    release_year = models.IntegerField(default=timezone.now().year)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    series = models.BooleanField(default=False)
    series_name = models.CharField(max_length=100, blank=True, null=True)
    series_season = models.IntegerField(blank=True, null=True)
    series_episode = models.IntegerField(blank=True, null=True)

    thumbnail = models.URLField(blank=True, null=True)
    subtitle = models.FilePathField(path='/home/atharvnaik/Desktop/Movies/',
                                    match='^.+\.(vtt|srt)$', recursive=True, blank=True, null=True)
    video = models.FilePathField(path='/home/atharvnaik/Desktop/Movies/',
                                 match='^.+\.(mkv|mp4)$', recursive=True, blank=True, null=True)

    video_file = models.FileField(upload_to=getFileUploadPath, validators=[
                                  validate_video_file], null=True, blank=True)
    preview_images = models.URLField(blank=True, null=True)

    genre = models.CharField(max_length=100, blank=True, null=True, choices=[
        ('Action', 'Action'),
        ('Adventure', 'Adventure'),
        ('Comedy', 'Comedy'),
        ('Crime', 'Crime'),
        ('Drama', 'Drama'),
        ('Romance', 'Romance'),
        ('Fantasy', 'Fantasy'),
        ('Horror', 'Horror'),
        ('Science Fiction', 'Science Fiction'),
        ('Thriller', 'Thriller'),
        ('Mystery', 'Mystery'),
        ('Historical', 'Historical'),
        ('Historical Fiction', 'Historical Fiction'),
        ('Philosophical', 'Philosophical'),
        ('Political', 'Political'),
    ])

    language = models.CharField(max_length=100, blank=True, null=True, choices=[
        ('English', 'English'),
        ('Hindi', 'Hindi'),
        ('Marathi', 'Marathi'),
        ('Kannada', 'Kannada'),
        ('Tamil', 'Tamil'),
        ('Telugu', 'Telugu'),
        ('Malayalam', 'Malayalam'),
        ('Bengali', 'Bengali'),
        ('Punjabi', 'Punjabi'),
        ('Gujarati', 'Gujarati'),
    ], default='English')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_duration(self):
        try:
            video = mp.VideoFileClip(self.video_file.path)
            return video.duration
        except:
            return 0


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    # get the video timestamp upto which the user has watched the video from the frontend
    timestamp = models.IntegerField(default=0)
    percentage_watched = models.FloatField(default=0)
    last_viewed = models.DateTimeField(auto_now=True)

    # calculate the percentage of the video watched before saving the history object
    def save(self, *args, **kwargs):
        video_duration = self.video.get_duration()
        # create a new field in the history model to store the percentage of the video watched
        self.percentage_watched = (self.timestamp / video_duration) * 100
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-last_viewed']

    def __str__(self):
        return f'{self.user.username} watched {self.video.title}'
