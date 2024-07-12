from django.db import models
from django.contrib.auth.models import User
from shortuuid.django_fields import ShortUUIDField
from django.utils import timezone
from .validators import validate_video_file, validate_subtitle_file, validate_upload_image_file
from .uploadpathsetters import getVideoUploadPath, getSubtitleUploadPath, getThumbnailUploadPath, getChannelAvatarUploadPath, getChannelBannerUploadPath
import moviepy.editor as mp
from .defaultpicsetters import getRandomDefaultPic
import shortuuid

# Create your models here.


class Channel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    channel_id = ShortUUIDField(
        length=22, default=shortuuid.uuid, primary_key=True, editable=False, unique=True)
    handle = models.CharField(
        max_length=100, unique=True, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to=getChannelAvatarUploadPath, validators=[validate_upload_image_file], null=True, blank=True)
    banner = models.ImageField(
        upload_to=getChannelBannerUploadPath, validators=[validate_upload_image_file], null=True, blank=True)
    
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = getRandomDefaultPic(self.user.first_name, self.user.last_name)
        super().save(*args, **kwargs)




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


class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=5000, null=True, blank=True)
    video_id = ShortUUIDField(
        length=11, default=shortuuid.uuid, primary_key=True, editable=False, unique=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    release_year = models.PositiveSmallIntegerField(default=timezone.now().year)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    series = models.BooleanField(default=False)
    series_name = models.CharField(max_length=100, blank=True, null=True)
    series_season = models.PositiveIntegerField(blank=True, null=True)
    series_episode = models.PositiveIntegerField(blank=True, null=True)

    thumbnail = models.FileField(upload_to=getThumbnailUploadPath, validators=[validate_upload_image_file], null=True, blank=True)
    subtitle = models.FileField(upload_to=getSubtitleUploadPath, validators=[
                                  validate_subtitle_file], null=True, blank=True)

    video_file = models.FileField(upload_to=getVideoUploadPath, validators=[
                                  validate_video_file], null=True, blank=True)
    
    video_location = models.CharField(max_length=100, choices=[
        ('local', 'Main Server (Local)'),
        ('s3', 'Cloud Server (S3)')
    ], default="local")

    stream_url = models.URLField(null=True, blank=True)
    
    duration = models.PositiveIntegerField(default=0)

    visibility = models.CharField(max_length=100, choices=[
        ('public', 'Public'),
        ('unlisted', 'Unlisted'),
        ('private', 'Private')
    ], default='public')

    subtitles_available = models.BooleanField(default=False)

    genre = models.CharField(max_length=100, blank=True, null=True, choices=[
        ('Action', 'Action'),
        ('Adventure', 'Adventure'),
        ('Anime', 'Anime'),
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
        ('Documentary', 'Documentary'),
        ('Biographical', 'Biographical'),
        ('Educational', 'Educational'),
        ('Musical', 'Musical'),
        ('Other', 'Other')
    ])

    language = models.CharField(max_length=100, blank=True, null=True, choices=[
        ('eng', 'English'),
        ('hin', 'Hindi'),
        ('jap', 'Japanese'),
        ('kor', 'Korean'),
        ('oth', 'Other'),
    ], default='eng')

    views = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        # check series name, episode and season not null if series is true
        constraints = [
            models.CheckConstraint(
                check=~models.Q(series=True) | ~models.Q(series_name=None), name='series_name_not_null'),
            models.CheckConstraint(
                check=~models.Q(series=True) | ~models.Q(series_season=None), name='series_season_not_null'),
            models.CheckConstraint(
                check=~models.Q(series=True) | ~models.Q(series_episode=None), name='series_episode_not_null'),
        ]

    def __str__(self):
        return self.title

    def get_duration(self):
        try:
            video = mp.VideoFileClip(self.video_file.path)
            return video.duration
        except:
            return 0
    
    def save(self, *args, **kwargs):
        if self.subtitle:
            self.subtitles_available = True
        super().save(*args, **kwargs)


class History(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, null=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    # get the video timestamp upto which the user has watched the video from the frontend
    timestamp = models.IntegerField(default=0)
    percentage_watched = models.FloatField(default=0)
    last_viewed = models.DateTimeField(auto_now=True)

    # calculate the percentage of the video watched before saving the history object
    def save(self, *args, **kwargs):
        video_duration = self.video.duration
        # create a new field in the history model to store the percentage of the video watched
        self.percentage_watched = (self.timestamp / video_duration) * 100
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-last_viewed']
        # make sure that a user can only have one history object for a video
        unique_together = ['channel', 'video']
        verbose_name_plural = 'Histories'

    def __str__(self):
        return f'{self.channel} watched {self.video.title}'
