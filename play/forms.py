from django.forms import ModelForm
from django import forms
from .models import Channel, Video


class SignInForm(ModelForm):
    class Meta:
        model = Channel
        fields = ['handle']

class VideoUploadForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Video
        fields = ['title', 'description', 'genre', 'release_year', 'language', 'series', 'series_name', 'series_season', 'series_episode', 'thumbnail', 'subtitle', 'visibility', 'video_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'text-input'}),
            'description': forms.Textarea(attrs={'class': 'text-input'}),
            'genre': forms.Select(attrs={'class': 'select-input'}),
            'release_year': forms.NumberInput(attrs={'class': 'text-input'}),
            'language': forms.Select(attrs={'class': 'select-input'}),
            'series': forms.CheckboxInput(attrs={'class': 'checkbox-input'}),
            'series_name': forms.TextInput(attrs={'class': 'text-input'}),
            'series_season': forms.NumberInput(attrs={'class': 'text-input'}),
            'series_episode': forms.NumberInput(attrs={'class': 'text-input'}),
            'video_file': forms.FileInput(attrs={'class': 'file-input'}),
            'thumbnail': forms.FileInput(attrs={'class': 'file-input'}),
            'subtitle': forms.FileInput(attrs={'class': 'file-input'}),
            'visibility': forms.Select(attrs={'class': 'select-input'}),
        }

    