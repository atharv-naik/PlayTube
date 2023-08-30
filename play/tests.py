from django.test import TestCase
from django.contrib.auth.models import User
from .models import Video
from django.core.files.uploadedfile import SimpleUploadedFile, InMemoryUploadedFile, TemporaryUploadedFile, UploadedFile
from django.urls import reverse

# Create your tests here.

class VideoTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_channel_creation(self):
        self.assertEqual(self.user.channel.name, 'testuser')
        self.assertEqual(self.user.channel.user, self.user)

    def test_video_upload(self):
        self.client.login(username='testuser', password='12345')

        video_file=SimpleUploadedFile('test_video.mp4', b'file_content', content_type='video/mp4')

        response = self.client.post(reverse('play:upload-video'), {'title': 'New Video', 'video_file': video_file, 'description': 'New Description', 'visibility': 'public', 'genre': 'Other', 'language': 'eng', 'channel': self.user.channel, 'release_year': 2020})

        self.client.logout()
        # assert if redirected to home page or redirected back to upload page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Video.objects.count(), 1)
    
    def test_video_upload_without_login(self):
        video_file=SimpleUploadedFile('test_video.mp4', b'file_content', content_type='video/mp4')

        response = self.client.post(reverse('play:upload-video'), {'title': 'New Video', 'video_file': video_file, 'description': 'New Description', 'visibility': 'public', 'genre': 'Other', 'language': 'eng', 'channel': self.user.channel, 'release_year': 2020})

        # assert if redirected to home page or redirected back to upload page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Video.objects.count(), 0)

    def test_video_upload_with_invalid_file(self):
        self.client.login(username='testuser', password='12345')

        video_file=SimpleUploadedFile('test_video.xyz', b'file_content')

        response = self.client.post(reverse('play:upload-video'), {'title': 'New Video', 'video_file': video_file, 'description': 'New Description', 'visibility': 'public', 'genre': 'Other', 'language': 'eng', 'channel': self.user.channel, 'release_year': 2020})

        self.client.logout()
        # assert if redirected to home page or redirected back to upload page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Video.objects.count(), 0)
    
    def test_video_upload_with_file_size_exceeding_limit(self):
        self.client.login(username='testuser', password='12345')

        video_file=TemporaryUploadedFile('test_video_large.mp4', 'video/mp4', 1024*1024*1024, 'utf-8')

        response = self.client.post(reverse('play:upload-video'), {'title': 'New Video', 'video_file': video_file, 'description': 'New Description', 'visibility': 'public', 'genre': 'Other', 'language': 'eng', 'channel': self.user.channel, 'release_year': 2020})

        self.client.logout()
        # assert if redirected to home page or redirected back to upload page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Video.objects.count(), 0)
