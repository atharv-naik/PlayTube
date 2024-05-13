from django.forms import ModelForm
from django import forms
from .models import Channel, Video
from django.utils import timezone


class SignInForm(ModelForm):
    class Meta:
        model = Channel
        fields = ['handle']

class VideoUploadForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Video
        fields = ['title', 'description', 'genre', 'release_year', 'language', 'series', 'series_name', 'series_season', 'series_episode', 'thumbnail', 'subtitle', 'visibility', 'video_file', 'video_location']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'text-input', 'placeholder': 'Add a title that describes your video', 'autofocus': True, 'autocomplete': 'off', 'required': True, 'maxlength': 100, 'minlength': 1, 'autocapitalize': 'on', 'spellcheck': 'true'}),
            'description': forms.Textarea(attrs={'class': 'text-input', 'placeholder': 'Tell viewers about your video', 'rows': 4, 'cols': 15}),
            'genre': forms.Select(attrs={'class': 'select-input', 'placeholder': 'Select a genre', 'autofocus': True, 'required': True}),
            'release_year': forms.NumberInput(attrs={'class': 'text-input', 'placeholder': 'Year', 'min': 1900, 'max': timezone.now().year, 'step': 1, 'type': 'text', 'pattern': '[0-9]{4}'}),
            'language': forms.Select(attrs={'class': 'select-input', 'placeholder': 'Select a language', 'autofocus': True}),
            'series': forms.CheckboxInput(attrs={'class': 'checkbox-input'}),
            'series_name': forms.TextInput(attrs={'class': 'text-input'}),
            'series_season': forms.NumberInput(attrs={'class': 'text-input'}),
            'series_episode': forms.NumberInput(attrs={'class': 'text-input'}),
            'video_file': forms.FileInput(attrs={'class': 'file-input', 'accept': '.mp4, .mkv'}),
            'thumbnail': forms.FileInput(attrs={'class': 'file-input', 'accept': '.png, .jpg, .jpeg'}),
            'subtitle': forms.FileInput(attrs={'class': 'file-input', 'accept': '.vtt, .srt'}),
            'visibility': forms.Select(attrs={'class': 'select-input', 'placeholder': 'Visibility'}),
            'video_location': forms.Select(attrs={'class': 'select-input', 'placeholder': 'Choose server'}),
        }
