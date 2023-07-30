from django.forms import ModelForm
from django import forms
from .models import Channel, Video


class SignInForm(ModelForm):
    class Meta:
        model = Channel
        fields = ['handle']

class VideoUploadForm(ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'genre', 'release_year', 'language', 'series', 'series_name', 'series_season', 'series_episode', 'video_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'video_file': forms.FileInput(attrs={'class': 'form-control'}),
        }

    