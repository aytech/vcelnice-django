from django import forms
from .models import Video


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['caption', 'description', 'youtube_id', 'thumb']
